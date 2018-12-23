##How do I drive this?

1. Select block for yourself and say to others that you have taken it
2. Remember to A) put right cache location in file cachehandler.py's CACHE_DB_LOCATION variable B) select correct input file for test program
3. Start rolling with next tests in that order, but notice that you can also jump some over and run earlier later straight from cache. Lets see if these are sensible ones.

| Tests |
| ----- |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 3, 2, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 4, 2, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 4, 3, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 2, 4, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 3, 4, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 4, 4, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 5, 4, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 6, 4, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 6, 4, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 4, 5, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 4, 6, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 6, 6, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 8, 6, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 6, 8, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 8, 8, use_wildcards=True)` |
| `ngra = GoogleNgramAlgorithm(row[1], row[0], 10, 10, use_wildcards=True)` |


4. Save results to result folder of block with reasonable name

After runs, run every test again but with last parameter False. This should take no time because all queries will be found in cache. Run and save them too accordingly

Explanations why:
* First run must be block sized with 12 because it has max efficiency (2x3x2x2=24 because sense size 2, contex size 2 and every bigram is queried with backwards also so its x2 and wildcard queries doulbe every query) because is asks always full maximum 12 blocks.
* Other larger runs have unknown amount of info from cache so we cannot predict any full-block efficiency so making it divided by 12 is not no important anymore
* No any use_wildcard=False queries anymore because they will be easy to run straight from cache
* Caching efficiency will be maximum if one person computes one block himself. Thats why splitting text material instead of fully running it.

Lets consider also some special runs like 2,8 and 8,2 or something later...