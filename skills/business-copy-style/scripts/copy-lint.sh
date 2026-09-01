#!/bin/sh
# copy-lint.sh — deterministic quality gate for customer-facing copy.
# Reports the metrics the eval cycle depends on and exits non-zero when a
# hard gate fails, so an agent can loop: draft -> lint -> revise -> lint -> ship.
#
# Usage:
#   copy-lint.sh [--max-grade N] [--max-emdash N] [--max-sentence N] FILE
#   copy-lint.sh [--structure] [structural threshold flags] FILE
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
# Pass --structure to add cadence, repetition, paragraph-load and scaffold counts.

set -eu

max_grade=6
max_emdash=0
max_sentence=15
structure=0
similar_length_tolerance=2
similar_run_min=3
max_paragraph_words=120
max_paragraph_sentences=6
file=""

require_value() {
  option="$1"
  value="${2-}"
  case "$value" in
    ""|-*)
      echo "copy-lint: $option requires a value" >&2
      exit 2
      ;;
  esac
}

while [ $# -gt 0 ]; do
  case "$1" in
    --max-grade) require_value "$@"; max_grade="$2"; shift 2 ;;
    --max-emdash) require_value "$@"; max_emdash="$2"; shift 2 ;;
    --max-sentence) require_value "$@"; max_sentence="$2"; shift 2 ;;
    --structure) structure=1; shift ;;
    --similar-length-tolerance)
      require_value "$@"; similar_length_tolerance="$2"; shift 2 ;;
    --similar-run-min) require_value "$@"; similar_run_min="$2"; shift 2 ;;
    --max-paragraph-words)
      require_value "$@"; max_paragraph_words="$2"; shift 2 ;;
    --max-paragraph-sentences)
      require_value "$@"; max_paragraph_sentences="$2"; shift 2 ;;
    -h|--help)
      sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'
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

# Tier and advisory phrase lists kept in sync with references/de-ai-prose.md.
# Base forms only; the matcher also catches -s/-d/-ed/-ing inflections.
tier1="delve landscape tapestry paradigm leverage harness navigate realm embark journey myriad plethora multifaceted revolutionize synergy ecosystem resonate streamline"
tier2="robust seamless cutting-edge innovative comprehensive pivotal nuanced compelling transformative bolster underscore foster imperative intricate overarching unprecedented groundbreaking elevate empower unlock spearhead"
stopwords="a about after again against all am an and any are as at be because been before being below between both but by can could did do does doing down during each few for from further had has have having he her here hers herself him himself his how i if in into is it its itself just me more most my myself no nor not of off on once only or other our ours ourselves out over own same she should so some such than that the their theirs them themselves then there these they this those through to too under until up very was we were what when where which while who whom why will with would you your yours yourself yourselves"
firstperson="i my mine we our ours"
contrast_phrases="not just|not only|more than just|i'm not|i am not|this isn't|this is not|we don't just|we do not just"
meta_phrases="what this means|the takeaway|in this section|on this page|as you can see|let's break|let us break|here's what|here is what|below you'll|below you will"

printf '%s' "$text" | awk \
  -v max_grade="$max_grade" -v max_emdash="$max_emdash" -v max_sentence="$max_sentence" \
  -v structure="$structure" -v length_tolerance="$similar_length_tolerance" \
  -v run_min="$similar_run_min" -v max_paragraph_words="$max_paragraph_words" \
  -v max_paragraph_sentences="$max_paragraph_sentences" \
  -v tier1="$tier1" -v tier2="$tier2" -v stopwords="$stopwords" \
  -v firstperson="$firstperson" -v contrast_phrases="$contrast_phrases" \
  -v meta_phrases="$meta_phrases" '
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
function trim(value){
  gsub(/^[[:space:]]+|[[:space:]]+$/, "", value)
  return value
}
function word_count(value,   clean,parts,count){
  clean=tolower(value); gsub(/[^a-z0-9-]+/, " ", clean); clean=trim(clean)
  if(clean=="") return 0
  count=split(clean,parts,/ +/)
  return count
}
function sentence_total(value,   tmp,count){
  tmp=value; count=gsub(/[.!?]+/, "", tmp)
  if(count<1 && trim(value)!="") count=1
  return count
}
function count_phrase(haystack,needle,   count,offset,found,rest){
  count=0; offset=1
  while(offset<=length(haystack)){
    rest=substr(haystack,offset)
    found=index(rest,needle)
    if(found==0) break
    count++
    offset += found + length(needle) - 1
  }
  return count
}
function count_comma_not(haystack,   count,rest){
  count=0; rest=haystack
  while(match(rest, /,[[:space:]]+not[[:space:]]+(a|an|the|this|that|these|those|my|our|your|their|its|his|her|any|some|no|every|each|one|two|three|four|five|six|seven|eight|nine|ten)[[:space:]]+[a-z]+/)){
    count++
    rest=substr(rest,RSTART+RLENGTH)
  }
  return count
}
function close_run(size){
  if(size>=run_min){ similar_runs++; if(size>longest_run) longest_run=size }
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

  if(structure){
    ns=split(stopwords,sw," "); for(i=1;i<=ns;i++) stopset[sw[i]]=1
    nf=split(firstperson,fp," "); for(i=1;i<=nf;i++) firstset[fp[i]]=1

    raw=full
    sentence_parts=split(raw,raw_sentences,/[.!?]+/)
    structural_sentences=0; total_sentence_words=0; first_person_starts=0
    for(i=1;i<=sentence_parts;i++){
      sentence=tolower(trim(raw_sentences[i])); gsub(/[^a-z0-9-]+/," ",sentence); sentence=trim(sentence)
      if(sentence=="") continue
      structural_sentences++
      sentence_words=split(sentence,sentence_tokens,/ +/)
      sentence_lengths[structural_sentences]=sentence_words
      total_sentence_words+=sentence_words
      duplicate_sentence[sentence]++
      if(sentence_words>=2) starter[sentence_tokens[1] " " sentence_tokens[2]]++
      if(firstset[sentence_tokens[1]]) first_person_starts++
      for(k=1;k<=sentence_words-3;k++){
        content=0
        for(j=0;j<4;j++) if(!stopset[sentence_tokens[k+j]]) content++
        if(content<2) continue
        phrase=sentence_tokens[k] " " sentence_tokens[k+1] " " sentence_tokens[k+2] " " sentence_tokens[k+3]
        fourgram[phrase]++
      }
    }

    duplicate_instances=0
    for(key in duplicate_sentence) if(duplicate_sentence[key]>1) duplicate_instances+=duplicate_sentence[key]-1
    starter_instances=0
    for(key in starter) if(starter[key]>1) starter_instances+=starter[key]-1

    stdev=0
    if(structural_sentences>1){
      mean=total_sentence_words/structural_sentences; squares=0
      for(i=1;i<=structural_sentences;i++) squares+=(sentence_lengths[i]-mean)^2
      stdev=sqrt(squares/structural_sentences)
    }

    similar_runs=0; longest_run=0; run_size=0
    for(i=1;i<=structural_sentences;i++){
      sentence_length=sentence_lengths[i]
      if(run_size==0){ run_size=1; run_low=sentence_length; run_high=sentence_length; continue }
      next_low=(sentence_length<run_low?sentence_length:run_low); next_high=(sentence_length>run_high?sentence_length:run_high)
      if(next_high-next_low<=length_tolerance){ run_size++; run_low=next_low; run_high=next_high }
      else { close_run(run_size); run_size=1; run_low=sentence_length; run_high=sentence_length }
    }
    close_run(run_size)

    repeated_fourgrams=0
    for(key in fourgram) if(fourgram[key]>1) repeated_fourgrams+=fourgram[key]-1
    fourgram_rate=repeated_fourgrams*1000/words

    overloaded_paragraphs=0; paragraph=""
    longest_paragraph_words=0; longest_paragraph_sentences=0
    for(i=1;i<=m+1;i++){
      line=(i<=m?lines[i]:"")
      if(trim(line)==""){
        if(trim(paragraph)!=""){
          pw=word_count(paragraph); ps=sentence_total(paragraph)
          if(pw>longest_paragraph_words) longest_paragraph_words=pw
          if(ps>longest_paragraph_sentences) longest_paragraph_sentences=ps
          if(pw>max_paragraph_words || ps>max_paragraph_sentences) overloaded_paragraphs++
          paragraph=""
        }
      } else paragraph=paragraph " " line
    }

    lower=tolower(raw)
    contrast_count=count_comma_not(lower); nc=split(contrast_phrases,contrast,/\|/)
    for(i=1;i<=nc;i++) contrast_count+=count_phrase(lower,contrast[i])
    meta_count=0; nm=split(meta_phrases,meta,/\|/)
    for(i=1;i<=nm;i++) meta_count+=count_phrase(lower,meta[i])
    first_rate=(structural_sentences?first_person_starts*100/structural_sentences:0)

    printf "----------------\n"
    printf "structural advisory (never gates)\n"
    printf "repetition: duplicate sentences %d | repeated starters %d | repeated 4-word phrases %d (%.1f/1k words)\n", \
      duplicate_instances, starter_instances, repeated_fourgrams, fourgram_rate
    printf "rhythm/load: sentence stdev %.1f | similar-length runs %d (longest %d) | overloaded paragraphs %d\n", \
      stdev, similar_runs, longest_run, overloaded_paragraphs
    printf "voice/scaffolds: first-person starts %.1f%% | contrast %d | meta phrases %d\n", \
      first_rate, contrast_count, meta_count
  }

  printf "----------------\n"
  if(grade>max_grade+0.05){ printf "FAIL grade %.1f > %s\n", grade, max_grade; fail=1 } else printf "pass  grade\n"
  if(emdash>max_emdash){ printf "FAIL em dashes %d > %s\n", emdash, max_emdash; fail=1 } else printf "pass  em dashes\n"
  if(t1n>0){ printf "FAIL Tier-1 vocab %d > 0\n", t1n; fail=1 } else printf "pass  Tier-1 vocab\n"
  if(avg>max_sentence+0.05){ printf "FAIL avg sentence %.1f > %s words\n", avg, max_sentence; fail=1 } else printf "pass  avg sentence length\n"

  exit (fail? 1 : 0)
}
'
