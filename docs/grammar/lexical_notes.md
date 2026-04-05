# Lexical Notes for Grammar

This document records lexical items with unusual behavior or edge cases
that require discussion in the grammar.

## samzang 'hair'

**Form:** samzang (atomic, not analyzable as sam+zang)

**Distribution:** 8 occurrences in corpus, all meaning 'hair':
- Judges 20:16 "at an hair breadth" 
- 1 Samuel 14:45 "not one hair of his head fall"
- 2 Samuel 14:11 "not one hair of thy son fall"  
- 1 Kings 1:52 "not an hair of him fall"
- Psalms 69:4 "hairs of mine head"
- Proverbs 23:7 (contextual usage)
- Matthew 5:36 "one hair white or black"
- Luke 21:18 "not an hair of your head perish"

**Note:** Not to be confused with compositional 'sam-zang' which would mean
'throw-INSTR' or 'open-use'. The word samzang is lexicalized as 'hair'.

## kapin 'weep-CVB'

**Form:** kap-in (compositional: kap 'weep' + -in CVB)

**Distribution:** 44 occurrences in corpus. 43 (97.7%) clearly mean 'weeping':
- Pattern: `X kapin a thum` = "X weeping they mourn"
- Typically co-occurs with thum 'mourn' in mourning contexts

**Edge Case - Judges 20:16:**

```
suang tawh samzang kapin a khial lo
stone with hair ?? NEG miss NEG
"could sling stones at an hair breadth and not miss"
```

In this single occurrence, `samzang kapin` appears in a precision/accuracy
context ("at a hair's breadth") rather than a weeping context. Possible
interpretations:

1. **Idiomatic:** 'hair touching' = 'precisely, exactly' (precision idiom)
2. **Different lexeme:** A homophonous kapin meaning 'to touch/reach'
3. **Weep (metaphorical):** The hair "weeps" = reaches the target

The analyzer treats this as kapin 'weep-CVB' since it's an isolated case.
Further research with native speakers needed to determine if this represents
a distinct lexeme or an idiomatic extension.

**Recommendation:** Note this passage in the grammar as requiring further
investigation. The 97.7% accuracy of 'weep-CVB' analysis is sufficient for
corpus-wide glossing.
