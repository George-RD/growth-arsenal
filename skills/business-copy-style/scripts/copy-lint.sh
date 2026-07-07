#!/bin/sh
# copy-lint.sh — deterministic quality gate for customer-facing copy.
# Reports the metrics the eval cycle depends on and exits non-zero when a
# hard gate fails, so an agent can loop: draft -> lint -> revise -> lint -> ship.
#
# Usage:
#   copy-lint.sh [--max-grade N] [--max-emdash N] [--max-sentence N] FILE
#   copy-lint.sh --help
#
# Reads FILE, or stdin when FILE is "-". Pure POSIX sh + awk, no dependencies.
#
# Hard gates (failure -> exit 1):
#   Flesch-Kincaid grade   <= --max-grade    (default 6)
#   em dashes (U+2014)     <= --max-emdash   (default 0)
#   Tier-1 AI vocabulary   == 0              (always)
#   avg words/sentence     <= --max-sentence (default 15)
# Advisory (reported, never fails): Tier-2 vocab, double-hyphen, boldface lists.

set -eu

max_grade=6
max_emdash=0
max_sentence=15
file=""

while [ $# -gt 0 ]; do
  case "$1" in
    --max-grade) max_grade="$2"; shift 2 ;;
    --max-emdash) max_emdash="$2"; shift 2 ;;
    --max-sentence) max_sentence="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'
      exit 0 ;;
    -) file="-"; shift ;;
    -*) echo "copy-lint: unknown option $1" >&2; exit 2 ;;
    *) file="$1"; shift ;;
  esac
done

if [ -z "$file" ]; then
  echo "copy-lint: no input file (use FILE or - for stdin)" >&2
  exit 2
fi

if [ "$file" = "-" ]; then
  text="$(cat)"
elif [ -f "$file" ]; then
  text="$(cat "$file")"
else
  echo "copy-lint: no such file: $file" >&2
  exit 2
fi

# Tier lists kept in sync with references/de-ai-prose.md. Base forms only;
# the matcher also catches -s/-d/-ed/-ing inflections (silent-e aware).
tier1="delve landscape tapestry paradigm leverage harness navigate realm embark journey myriad plethora multifaceted revolutionize synergy ecosystem resonate streamline"
tier2="robust seamless cutting-edge innovative comprehensive pivotal nuanced compelling transformative bolster underscore foster imperative intricate overarching unprecedented groundbreaking elevate empower unlock spearhead"

printf '%s' "$text" | awk \
  -v max_grade="$max_grade" -v max_emdash="$max_emdash" -v max_sentence="$max_sentence" \
  -v tier1="$tier1" -v tier2="$tier2" '
function isvowel(c){ return (c ~ /[aeiouy]/) }
function syllables(w,   i,c,n,prev){
  n=0; prev=0
  for(i=1;i<=length(w);i++){ c=substr(w,i,1); if(isvowel(c)){ if(!prev) n++; prev=1 } else prev=0 }
  if(length(w)>2 && substr(w,length(w),1)=="e" && substr(w,length(w)-1,2)!="le" && n>1) n--
  if(n<1) n=1
  return n
}
function matches(w,term,   base){
  if(w==term || w==term"s" || w==term"d" || w==term"ed" || w==term"ing") return 1
  if(substr(term,length(term),1)=="e"){
    base=substr(term,1,length(term)-1)
    if(w==base"ing" || w==base"ed" || w==base"es") return 1
  }
  return 0
}
{ full = full $0 "\n" }
END{
  tmp=full; emdash=gsub(/—/,"",tmp)
  tmp=full; endash=gsub(/–/,"",tmp)
  tmp=full; dhyphen=gsub(/ -- /,"",tmp)

  tmp=full; sentences=gsub(/[.!?]+/,"",tmp); if(sentences<1) sentences=1

  clean=tolower(full); gsub(/[^a-z-]+/," ",clean)
  words=0; syl=0
  n=split(clean,arr," ")
  nt1=split(tier1,t1," "); nt2=split(tier2,t2," ")
  t1n=0; t2n=0
  for(i=1;i<=n;i++){
    w=arr[i]; gsub(/^-+|-+$/,"",w); if(w=="") continue
    words++; syl+=syllables(w)
    for(k=1;k<=nt1;k++){ if(matches(w,t1[k])){ t1n++; t1seen[t1[k]]++ } }
    for(k=1;k<=nt2;k++){ if(matches(w,t2[k])){ t2n++; t2seen[t2[k]]++ } }
  }
  if(words<1) words=1
  avg=words/sentences
  grade=0.39*avg + 11.8*(syl/words) - 15.59
  if(grade<0) grade=0

  t1list=""; for(k=1;k<=nt1;k++){ if(t1seen[t1[k]]>0) t1list=t1list sprintf(" %s(%d)",t1[k],t1seen[t1[k]]) }
  t2list=""; for(k=1;k<=nt2;k++){ if(t2seen[t2[k]]>0) t2list=t2list sprintf(" %s(%d)",t2[k],t2seen[t2[k]]) }

  boldlist=0
  m=split(full,lines,"\n")
  for(i=1;i<=m;i++){ if(lines[i] ~ /^[ \t]*[-*][ \t]+\*\*/) boldlist++ }

  fail=0
  printf "copy-lint report\n"
  printf "----------------\n"
  printf "words / sentences        : %d / %d (avg %.1f words/sentence)\n", words, sentences, avg
  printf "Flesch-Kincaid grade     : %.1f\n", grade
  printf "em dashes (U+2014)       : %d\n", emdash
  printf "Tier-1 AI vocabulary     : %d%s\n", t1n, (t1n>0? t1list : "")
  printf "----------------\n"
  printf "advisory: en dashes %d | double-hyphen %d | Tier-2 %d%s | boldface list items %d\n", \
    endash, dhyphen, t2n, (t2n>0? t2list : ""), boldlist
  printf "----------------\n"
  if(grade>max_grade+0.05){ printf "FAIL grade %.1f > %s\n", grade, max_grade; fail=1 } else printf "pass  grade\n"
  if(emdash>max_emdash){ printf "FAIL em dashes %d > %s\n", emdash, max_emdash; fail=1 } else printf "pass  em dashes\n"
  if(t1n>0){ printf "FAIL Tier-1 vocab %d > 0\n", t1n; fail=1 } else printf "pass  Tier-1 vocab\n"
  if(avg>max_sentence+0.05){ printf "FAIL avg sentence %.1f > %s words\n", avg, max_sentence; fail=1 } else printf "pass  avg sentence length\n"

  exit (fail? 1 : 0)
}
'
