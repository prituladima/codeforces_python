```bash
conda env create -f .conda_env.yml
conda activate cf-stat
```

```bash
python generate_time.py CF_div2 C
```

```bash
python generate_time.py Leetcode Medium
```

# TODO
- Add time gate for call. In min. Like this:

```bash
python generate_time.py Leetcode Medium 25
```