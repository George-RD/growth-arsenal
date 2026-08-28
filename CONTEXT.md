# Growth Arsenal

Growth Arsenal is a set of linked business-growth workflows. This glossary names the concepts that matter when those workflows compose with other installable skills.

## Language

**Companion skill**:
An independently installable skill that another skill may invoke for a focused capability.
_Avoid_: inherited skill, plugin dependency

**Quality dependency**:
A companion skill whose absence allows the workflow to continue, but prevents it from claiming the full quality gate that skill provides.
_Avoid_: optional dependency

**Hard dependency**:
A companion skill whose absence blocks the specific workflow path that needs it.
_Avoid_: required plugin

**Dependency shim**:
The temporary resolve, explain, prompt and degrade behavior used while the standard Skills CLI has no native dependency resolution for the relationship.
_Avoid_: dependency manager, custom resolver

**Dependency watchpoint**:
Repository guidance that requires maintainers and agents to check current upstream Skills CLI support before extending the dependency shim.
_Avoid_: dependency roadmap
