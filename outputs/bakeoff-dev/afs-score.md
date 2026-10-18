| arm | D01 | D02 | D03 | D04 | D05 | D06 | D07 | D08 | mean recall |
|---|---|---|---|---|---|---|---|---|---|
| baseline | 5/5 | 4/4 | 4/4 | 4/4 | 1/2 | 3/5 | 3/4 | 6/8 | 82% |
| deepseek-1017 | 4/5 | 3/4 | 4/4 | 4/4 | 2/2 | 3/5 | 2/4 | 5/8 | 78% |
| gemini-3.5-flash-lite | 3/5 | 2/4 | 2/4 | 4/4 | 2/2 | 3/5 | 2/4 | 4/8 | 65% |
| gemini-3.8-flash | 5/5 | 3/4 | 3/4 | 4/4 | 2/2 | 3/5 | 3/4 | 6/8 | 82% |
| glm-5.3-flash | 4/5 | 4/4 | 3/4 | 4/4 | 2/2 | 3/5 | 3/4 | 7/8 | 85% |
| mix-a | 3/5 | 3/4 | 4/4 | 4/4 | 2/2 | 4/5 | 3/4 | 7/8 | 85% |
| mix-b | 4/5 | 3/4 | 3/4 | 4/4 | 2/2 | 3/5 | 2/4 | 5/8 | 75% |

| arm | case | AFS worked answer methods | primary | primary + comparison |
|---|---|---|---|---|
| baseline | D01 | NIR, Raman | NIR | NIR, Raman |
| baseline | D02 | NIR | NIR | MIR, NIR |
| deepseek-1017 | D01 | NIR, Raman | NIR | NIR, Raman |
| deepseek-1017 | D02 | NIR | NIR | NIR |
| gemini-3.5-flash-lite | D01 | NIR, Raman | NIR | NIR, Raman |
| gemini-3.5-flash-lite | D02 | NIR | NIR | MIR, NIR |
| gemini-3.8-flash | D01 | NIR, Raman | Raman | NIR, Raman |
| gemini-3.8-flash | D02 | NIR | NIR | MIR, NIR |
| glm-5.3-flash | D01 | NIR, Raman | NIR | NIR, Raman |
| glm-5.3-flash | D02 | NIR | NIR | MIR, NIR |
| mix-a | D01 | NIR, Raman | NIR | NIR, Raman |
| mix-a | D02 | NIR | NIR | NIR |
| mix-b | D01 | NIR, Raman | NIR | NIR, Raman |
| mix-b | D02 | NIR | NIR | MIR, NIR |
