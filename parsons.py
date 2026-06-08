import os
import random
import shutil

def parse_data(snippet_path: str, distractor_path: str) -> list[tuple[list[str], list[str]]]:
    s_files =   {f : f'{snippet_path}/{f}' for f in os.listdir(snippet_path)}
    d_files = {f : f'{distractor_path}/{f}' for f in os.listdir(distractor_path)}
    data = []
    for key in s_files:
        with open(s_files[key]) as f1:
            snippet = [ln.strip() for ln in f1]
        with open(d_files[key]) as f2:
            distractors = [ln.strip() for ln in f2]
        data.append((snippet, distractors))
    return data

def parsons_problem(code_snippet: list[str], distractors: list[str]) -> tuple[list[tuple[int, str]], list[int]]:
    all_lines = code_snippet + distractors
    indices = list(i+1 for i in range(len(all_lines)))
    random.shuffle(indices)
    scrambled = [(indices[i], line) for i, line in enumerate(all_lines)]
    solution = [indices[i] for i in range(len(code_snippet))]
    random.shuffle(scrambled)
    return scrambled, solution


if __name__ == "__main__":
    s_path = "snippets"
    d_path = "distractors"
    data = parse_data(snippet_path=s_path, distractor_path=d_path)
    problems = [parsons_problem(*d) for d in data]


    if os.path.exists("output"):
        shutil.rmtree("output")
    os.mkdir("output")
    with open("output/problems.md", "w") as pf, open("output/solutions.md", "w") as sf:
        for i, (scrambled, solution) in enumerate(problems, start=1):
            # Problems file
            pf.write(f"# Problem {i}\n\n```java\n")
            for idx, line in scrambled:
                pf.write(f"{idx}. {line}\n")
            pf.write("```\n\n")

            # Solutions file
            sf.write(f"# Problem {i}\n\n")
            sf.write(", ".join(str(s) for s in solution))
            sf.write("\n\n")