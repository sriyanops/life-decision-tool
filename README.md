# Life Decision Tool (v.o1)

A structured decision-making tool that helps you compare two options against the life boundaries you actually care about.
This tool is designed to **remove options that don’t fit your life**, then clearly compare what remains.

## Link to tool: https://life-decision-tool.streamlit.app




## What This Tool Does

The Life Decision Tool helps you:

1. **Define non-negotiable boundaries**
   - Money at risk
   - Time commitment
   - Stress & health load
   - Impact on relationships

2. **Describe two real options**
   - What they realistically cost
   - How much time they demand
   - How stressful they are
   - What they would change in day-to-day life

3. **Eliminate what doesn’t fit**
   - If an option crosses even one boundary, it’s removed
   - No trade-offs, no rationalizing

4. **Compare what remains**
   - Uses weighted criteria based on the type of decision (career, personal, etc.)
   - Produces a clear fit comparison
   - Still leaves the final choice to you

5. **Ground the result in reality**
   - Shows what would *actually* change in your daily life
   - Prevents “spreadsheet-brain” decisions



## What This Tool Does *Not* Do

- It does **not** tell you what to choose  
- It does **not** optimize for happiness, money, or success  
- It does **not** replace judgment, values, or responsibility  

It only shows you what fits the life you described.



## How It Works (High Level)

1. You lock your **limits** (non-negotiables)
2. You describe **Option A** and **Option B**
3. The tool runs a **boundary check**
4. Options that fail are removed
5. Remaining options are compared using weighted criteria
6. Final results are shown alongside real-world consequences



## Project Structure

```text
life-decision-tool/
│
├── src/
│   ├── app.py
│   ├── nav.py
│   ├── state.py
│   │
│   ├── screens/
│   │   ├── home.py
│   │   ├── category.py
│   │   ├── constraints.py
│   │   ├── options.py
│   │   ├── compare.py
│   │   ├── past.py
│   │   └── load.py
│   │
│   ├── models.py
│   └── criteria.py
│
├── assets/
│   └── THEBOLDFONT-FREEVERSION.ttf
│
├── requirements.txt
└── README.md
```

## Deployment

This app is designed to be deployed on Streamlit Cloud, so it can be used via a link without running anything locally.

## Philosophy

Most bad decisions don’t come from lack of intelligence.
They come from:

1. Ignoring constraints
2. Overvaluing upside
3. Underestimating daily costs

This tool exists to make those costs visible.

## Future Changes
1. Adding export PDF summary
2. Adding more choices

## Author

Built by Sriyan♡♡Dedicated to my Eesha 

