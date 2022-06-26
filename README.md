# Bayan: Towards an Effective Arabic Fatwa Search Engine

## Introduction

Bayan is an Arabic search engine built for the Islamic jurisprudence domain upon the Google search engine.

Bayan uses the *Google Custom Search JSON API* to search for an Islamic query on a list of specific authentic websites, which can be customized by the user. After the results are retreived, they are re-ranked based on a fine-tuned AraBERT model and displayed to the user through the web frontend, along with the annotation of Quran and Hadith verses.

We evaluated our re-ranking model using the existing SEMEVAL test set and our in-house test set, built specifically for our problem domain. We acheived a Macro F1 score of 85% on the SEMEVAL test set and an NDCG@10 score of 93.90% on the Bayan in-house test set.

## Collaborators

Students:
* Abdulrahman Al-Raimi
* Faisal Abughazaleh
* Saad Anis

Supervisor:
* Dr. Tamer Elsayed