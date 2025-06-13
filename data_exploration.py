#!/usr/bin/env python3

import pandas as pd
from datasets import load_dataset
import numpy as np

def explore_dataset():
    print("Loading HFforLegal/case-law dataset...")
    
    # Load a small subset for development
    try:
        dataset = load_dataset("HFforLegal/case-law", "default", split="train[:100]")
        print("Loaded first 100 examples for development")
    except:
        print("Failed to load subset, trying full dataset...")
        dataset = load_dataset("HFforLegal/case-law", "default")
    
    print(f"Dataset structure: {dataset}")
    
    # Handle different dataset formats
    if hasattr(dataset, 'train'):
        data = dataset['train']
        print(f"Train split size: {len(data)}")
    else:
        data = dataset
        print(f"Dataset size: {len(data)}")
    
    # Get first few examples
    first_example = data[0]
    print("\nFirst example fields:")
    for key, value in first_example.items():
        if key == 'document':
            print(f"{key}: {str(value)[:200]}..." if len(str(value)) > 200 else f"{key}: {value}")
        else:
            print(f"{key}: {value}")
    
    # Analyze document lengths
    print("\nAnalyzing document lengths...")
    doc_lengths = []
    for i in range(min(1000, len(data))):  # Sample first 1000 documents
        doc = data[i]['document']
        if doc:
            doc_lengths.append(len(doc))
    
    print(f"Average document length: {np.mean(doc_lengths):.0f} characters")
    print(f"Median document length: {np.median(doc_lengths):.0f} characters")
    print(f"Min document length: {np.min(doc_lengths)} characters")
    print(f"Max document length: {np.max(doc_lengths)} characters")
    
    # Show sample document
    print("\n" + "="*50)
    print("SAMPLE DOCUMENT:")
    print("="*50)
    sample_doc = data[0]
    print(f"Title: {sample_doc['title']}")
    print(f"Citation: {sample_doc['citation']}")
    print(f"State: {sample_doc['state']}")
    print(f"Document excerpt: {sample_doc['document'][:1000]}...")
    
    return dataset

if __name__ == "__main__":
    dataset = explore_dataset()