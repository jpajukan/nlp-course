# Natural Language Processing and Text Mining - Coursework Project

## Word sense disambiguation by Wikification and Google Books Ngram

This repository contains wikification in folder for Wikification word disambiguation and Google Books Ngram WSD Algorithm code and test are in folder ngram. Final course report in PDF format in root folder.

**NOTICE:** This project does not have any official connection to Google or Wikipedia, other than using tools they provide.

### Authors
* Jukka Pajukangas
* Joel Lehtela
* Lauri Haverinen
* Mikko Paasimaa
* Heikki Kaarlela

## Wikification

An algorithm for Python that uses Wikipedia API to disambiguate words in their given corpus. It compares the 10 most relevant search results of a word with the given corpus to find the most probable definition for given word.

Running instructions and other data can be found in the folder wikify.

## Google Books Ngram WSD Algorithm

Word sense disambiguation algorithm utilizing Google Books Ngram Viewer was created during this project. Algorithm utilizes Lesk-styled calculations to compare each possible word sense to its context while utilizing co-occurence information retreived from Google Books Ngram Viewer as a scoring system for each pair of words.

Running instructions and other data can be found at folder ngram.
