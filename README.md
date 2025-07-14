# AI-Powered-Document-Data-Extractor


![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=flat-square&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791?style=flat-square&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-24.0.0-2496ED?style=flat-square&logo=docker)
![NLP](https://img.shields.io/badge/NLP-Concepts-orange?style=flat-square)

## Overview

The **AI-Powered Document Data Extractor** is a robust web application designed to automate the extraction and parsing of key information from various document types. Built with Python and FastAPI, this tool streamlines the process of converting unstructured documents (PDF and DOCX) into structured, actionable data, which is then securely stored in a PostgreSQL database. While demonstrated with resumes, its core functionality is adaptable to any document requiring data extraction.

This project demonstrates core capabilities in:
* **AI Agent Development:** Automating intelligent data processing workflows.
* **Data Extraction & Parsing:** Converting complex document formats into usable data.
* **API Development:** Building a scalable and accessible web service.
* **Database Management:** Storing and retrieving structured information efficiently.
* **Foundational NLP:** Applying basic text processing techniques for information retrieval.

## Features

* **Document Upload:** Accepts files in PDF (`.pdf`) and DOCX (`.docx`) formats.
* **Text Extraction:** Extracts full textual content from uploaded documents.
* **Information Parsing:** Identifies and extracts key details such as:
    * Candidate Name (for resume-like documents)
    * Email Address
    * Phone Number
    * Recognized Skills (based on a predefined keyword list)
* **Database Storage:** Persists extracted and parsed document data into a PostgreSQL database.
* **RESTful API:** Provides a clean and accessible API endpoint for integration with other applications.
* **Interactive Documentation:** Includes auto-generated Swagger UI for easy API testing and exploration.

## Technologies Used

* **Backend:** Python 3.9+
* **Web Framework:** FastAPI
* **Database:** PostgreSQL
* **PDF Parsing:** `PyPDF2`
* **DOCX Parsing:** `python-docx`
* **Database Driver:** `psycopg2-binary`
* **Data Validation:** `pydantic`
* **Containerization:** Docker (for potential future deployment)
