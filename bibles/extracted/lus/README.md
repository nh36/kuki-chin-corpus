Parallel Bible Corpus
=====================

Bible Version
-------------

* __Title:__ Mizo Old Version Bible<br>The Bible in Mizo (Lushai)
* __Corpus ID:__ lus-x-bible-1959
* __Language name:__ Mizo (Lushai)
* __Closest ISO 639-3:__ lus
* __Year of translation:__ 1959
* __Source:__ <https://www.bible.com/de/bible/253/gen.1.miz>
* __Copyright:__ © Bible Society of India 1959
* __Copyright (long version):__ Mizo Old Version Bible<br>This translation was published by the Bible Society of India in 1959. If you are interested in obtaining a printed copy, please contact the Bible Society of India at bsico@vsnl.com.
* __Homepage:__ <http://paralleltext.info/data/lus-x-bible-1959>
* __Version:__ 959
* __Last modified:__ 2015-05-11

Resources
---------

* __Text of the Gospel according to Mark__  
	The text is unicode normalized and with punctuation separated by spaces from the preceding word. The first column lists the versenames, the second column contains the actual text. When the second column is empty, this indicates that the content of this versename is very probably translated together with the preceding versename. When a versename is not included, than there was no translation available for this verse.
	+ File: lus-x-bible-1959.txt
	+ Format: csv
* __Wordforms__  
	All wordsform in the complete text are listed in the first column, with frequency counts provided in the second column. The wordforms and the frequency counts are made for the complete text, not just for the Gospel according to Mark included in this data package. The line numbers of this file are necessary for the interpretation of the sparse matrix file.
	+ File: lus-x-bible-1959.wordforms
	+ Format: csv
* __Versenames__  
	List of all verses occurring somewhere in our complete Bible corpus (across all versions and all languages). The first two digits represent the book, the following three digits represent the chapter, and the final three digits represent the verse. The line numbers of this file are necessary for the interpretation of the sparse matrix file.
	+ File: versenames.txt
	+ Format: txt
* __Wordforms x verses matrix__  
	Sparse matrix in Matrix Market format, with line numbers of the wordforms as rows and line numbers of the the versenames as columns. This matrix includes the information for the complete text, not just for the Gospel according to Mark. This file thus provides information about exactly which wordforms that occur in each verse, but not in which order they occur. This matrix can be used to efficiently compute cross-linguistic coocurrence statistics, suggesting translational equivalents.
	+ File: lus-x-bible-1959.mtx
    + Format: mtx
* __Datapackage__  
	Computer-readable JSON file containing all information about this data package
	+ File: datapackage.json
	+ Format: json
* __Readme__  
	Readme in Markdown format.
	+ File: README.md
	+ Format: md

Format Description
------------------

The format for the Bible texts has the following structure. Each line contains two elements which are separated by a TAB. The first element is the verse ID and the second element contains the actual text. The verse ID contains information about the book, chapter and verse number and is structured as follows (for the example of the verse ID 40001003):

* the first two digits represent the number of the book (e.g. 40 refers to the first book in the New Testament, the Gospel according to Matthew). The correspondences between book names and numbers are given below.
* the next three digits indicate the chapter (e.g. 001 refers to the first chapter in the book)
* the last three digits show the verse number (e.g. 003 refers to the third verse in the chapter)

Some lines contain only a verse ID and a TAB, but no actual text. In these cases, the translation of the respective verse ID is combined into the last preceding full text line above the empty text line. For example, when ID 400001003 has no text, but ID 400001002 (directly preceding) contains text, then one can assume that the content of ID 400001003 is available somewhere inside that text of ID 400001002, but it is not easy to separate the content.

Bible Book IDs
--------------

* 01 : Genesis 
* 02 : Exodus 
* 03 : Leviticus 
* 04 : Numbers 
* 05 : Deuteronomy 
* 06 : Joshua 
* 07 : Judges 
* 08 : Ruth 
* 09 : 1 Samuel 
* 10 : 2 Samuel 
* 11 : 1 Kings 
* 12 : 2 Kings 
* 13 : 1 Chronicles 
* 14 : 2 Chronicles 
* 15 : Ezra 
* 16 : Nehemiah 
* 17 : Esther 
* 18 : Job 
* 19 : Psalms 
* 20 : Proverbs 
* 21 : Ecclesiastes 
* 22 : Song of Solomon 
* 23 : Isaiah 
* 24 : Jeremiah 
* 25 : Lamentations 
* 26 : Ezekiel 
* 27 : Daniel 
* 28 : Hosea 
* 29 : Joel 
* 30 : Amos 
* 31 : Obadiah 
* 32 : Jonah 
* 33 : Micah 
* 34 : Nahum 
* 35 : Habakkuk 
* 36 : Zephaniah 
* 37 : Haggai 
* 38 : Zechariah 
* 39 : Malachi 
* 40 : Matthew 
* 41 : Mark 
* 42 : Luke 
* 43 : John 
* 44 : Acts 
* 45 : Romans 
* 46 : 1 Corinthians 
* 47 : 2 Corinthians 
* 48 : Galatians 
* 49 : Ephesians 
* 50 : Philippians 
* 51 : Colossians 
* 52 : 1 Thessalonians 
* 53 : 2 Thessalonians 
* 54 : 1 Timothy 
* 55 : 2 Timothy 
* 56 : Titus 
* 57 : Philemon 
* 58 : Hebrews 
* 59 : James 
* 60 : 1 Peter 
* 61 : 2 Peter 
* 62 : 1 John 
* 63 : 2 John 
* 64 : 3 John 
* 65 : Jude 
* 66 : Revelation
* 67 : Tobit
* 68 : Judith
* 69 : Esther, Greek
* 70 : Wisdom of Solomon
* 71 : Ecclesiasticus (Sira
* 72 : Baruch
* 73 : Epistle of Jeremiah
* 74 : Prayer of Azariah
* 75 : Susanna
* 76 : Bel and the Dragon
* 77 : 1 Maccabees
* 78 : 2 Maccabees
* 79 : 3 Maccabees
* 80 : 4 Maccabees
* 81 : 1 Esdras
* 82 : 2 Esdras
* 83 : Prayer of Manasseh
* 84 : Psalm 151
* 85 : Psalm of Solomon
* 86 : Odes

Project
-------

* __Name:__ Parallel Bible Corpus
* __URL:__ <http://paralleltext.info>
* __Description:__ The Parallel Bible Corpus is an ongoing project that aims at collecting Bible texts from the world's languages with the inherent parallelism of the verses being preserved. The ultimate goal is to provide a large collection of language data from all continents and language families that can be used for language comparison on the text level. The texts are not collected with a liturgical goal, nor for the enhancement of bible study. Although we think that the current resource might also be valuable in that context, we are explicitly making a resource for comparative linguistics. We aim to represent the text as close as possible to the intended form of the original translation, and we give full credit and reference for all translations included in this corpus. We welcome all suggestions and corrections (cysouw@uni-marburg.de). However, please note that the texts in this corpus are not intended to be authoritative liturgical versions of the respective translations. Please consult the original version as indicated in our corpus to obtain the translation in its original context.  <br> The corpus is compiled and maintained by Thomas Mayer and Michael Cysouw within the Paralleltext.info project at the Philipps University of Marburg, with thankfully acknowledged assistance from Östen Dahl, Matthew Dryer, Harald Hammarström and Bernhard Wälchli. A summary of the goals and methods of the project can be found in: Mayer & Cysouw (in print) Creating a Massively Parallel Bible Corpus (http://paralleltext.info/).
 
Maintainers
-----------

* __Thomas Mayer__  
	<thommy.mayer@gmail.com>  
	<http://th-mayer.de>

* __Michael Cysouw__  
	<cysouw@uni-marburg.de>
	<http://cysouw.de>