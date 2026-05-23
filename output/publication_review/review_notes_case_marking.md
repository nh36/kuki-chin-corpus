# Review Notes: Tedim Case-Marking Print Slice

## 1. What works

The case-marking slice is the first place where the current Tedim pipeline begins to look like a publication workflow rather than a pure backend dashboard. Source routing is already useful: the grammar source map, case-marking report, literature review, and example-selection audit point to the same cluster of evidence, so editorial prose can be written without hunting across the repository blindly. Locative **-ah**, ablative **-pan**, and comitative **-tawh** already have stable, safe Bible examples that can be integrated into actual exposition. The generated outputs are also now deterministic enough that editorial drafting is not invalidated every time `make grammar-reports` is rerun.

The dictionary side is also good enough for a vertical-slice test. The backend sample files are not themselves print entries, but they are now stable evidence sets rather than noisy dumps. That makes it possible to recast them as short, reader-facing entries with grammar cross-references and explicit editorial status.

## 2. What does not yet work

The slice also shows clearly what still requires manual editorial work. The biggest problem is ergative **-in**. The descriptive claim is secure in the literature, but the current backend cannot yet distinguish nominal ergative **-in** cleanly from converbal, quotative, and other homographic strings. That means the grammar can describe ergative marking, but it cannot yet print an automatically selected Bible example without risk of error.

More generally, the generated grammar outputs remain synthesis aids, not finished prose. They surface safe examples and routed sources, but they do not themselves decide how much of the spatial system belongs under case markers and how much belongs under relator nouns. Likewise, the backend dictionary labels are still too noisy for direct print use: they provide evidence, not editorially shaped entries.

## 3. Recommended next editorial task

The next task should be **reviewing this case-marking slice itself**, with one concrete question in mind: is the current balance between case markers and relator nouns the right print-facing shape? If the answer is yes, the next slice should probably move to **pronominal marking** or **TAM**, since both have enough routed material to test another coherent section of the package. If the answer is no, the first correction should be narrowly targeted: manually select one or two secure Bible examples for ergative **-in** and decide how to present relator nouns in the final grammar chapter before expanding further.
