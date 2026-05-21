---
layout: post
title: "Online Fake News Detection using Convolutional Neural Networks and Transformers"
date: 2024-04-28
categories: deep-learning
description: "A deep learning framework comparing pre-trained Transformer embeddings and CNN architectures to classify and detect online misinformation."
related_posts: false
---

Misinformation and fake news on social media represent a significant threat to political, economic, and social stability. As part of a collaborative final project for _CS 7643: Deep Learning_ at Georgia Tech in Spring 2024, our team ("News Detectives") designed and benchmarked a deep learning pipeline to automate the detection of online fake news. We compared the performance of Convolutional Neural Networks (CNNs) and sequence-to-sequence Transformers, specifically **BERT** and **RoBERTa**.

---

## 1. The Dataset Landscape

To train and validate our models, we leveraged three distinct datasets:

1. **The Kaggle "Fake and Real News" Dataset**: Our primary training corpus. It contains thousands of articles labeled with detailed metadata including title, author, text body, and specific classification types such as "bias", "conspiracy", "BS", and "fake".
2. **Organized News Articles Dataset**: A secondary cleaned corpus used to verify semantic consistency.
3. **Syrian War Fake News Dataset**: An out-of-domain dataset used specifically for validation. This allowed us to evaluate how well our models generalize to unseen political contexts and novel events, avoiding the common pitfall of topic-specific memorization.

---

## 2. Methodology & Architectures

Our pipeline focused on extracting semantic features from both the headline titles and the full text of articles. We explored two major deep learning methodologies:

### A. Pre-trained Transformers (BERT & RoBERTa)

We utilized **BERT** (Bidirectional Encoder Representations from Transformers) and **RoBERTa** (Robustly Optimized BERT Pretraining Approach) as feature extractors.

- **Feature Extraction**: Articles and titles were tokenized and passed through the pre-trained models to extract dense semantic vector embeddings.
- **Fine-Tuning**: To adapt the models to classification, we added custom classification heads. These heads consisted of fully connected (dense) layers, dropout layers to prevent overfitting, and max pooling.
- **Optimization**: The entire pipeline was optimized using the **Adam** optimizer, minimizing **cross-entropy loss**.

### B. Convolutional Neural Networks (CNNs)

In addition to Transformers, we implemented CNNs tailored for natural language processing (NLP).

- **Word Embeddings**: Words were mapped to dense vectors using pre-trained embeddings (Word2Vec/GloVe) and TF-IDF representations.
- **1D Convolutions**: We applied 1D convolutional filters of varying sizes (bigrams, trigrams, and four-grams) to capture local contextual patterns in the text.
- **Pooling**: Global max pooling was applied to extract the most salient features before passing them to a fully connected classifier.

{% include figure.liquid path="/assets/img/fake_news_pipeline.png" title="Figure 1: Deep Learning Text Classification Pipeline - Pre-trained Transformer Encoder (BERT/RoBERTa) vs. 1D CNN Architectures" class="img-fluid rounded z-depth-1" %}

> [!IMPORTANT]
> Because Transformer feature extraction involves massive pre-trained weights that remain fixed or are fine-tuned, they capture bidirectionally deep semantic relationships. In contrast, 1D CNNs rely on local n-gram window convolutions, making them faster to train but more sensitive to stylistic choice rather than actual factuality.

---

## 3. Error Analysis and Model Limitations

A key focus of our research was performing a detailed error analysis of misclassified articles. We observed that:

- **Sarcasm and Satire**: Models frequently misclassified satirical articles (like _The Onion_) as news because they mimic the syntactic structure and vocabulary of real news reports.
- **Topic Bias**: Models trained purely on U.S. political datasets initially struggled on our out-of-domain validation dataset (the Syrian War corpus), highlighting the need for domain-agnostic pre-training and diverse validation datasets.
- **Factuality vs. Style**: CNN models are highly sensitive to writing style and specific keywords, whereas Transformer models (BERT/RoBERTa) demonstrate a much better grasp of overall article context and semantic consistency.

---

## 4. Evaluation and Future Directions

Our models were evaluated using standard metrics: accuracy, precision, recall, and F1-score. Pre-trained Transformer models demonstrated superior F1-scores, illustrating their ability to model complex dependencies and contextual nuances compared to standard CNNs.

Potential future directions for this work include:

1. **Multimodal Fusion**: Incorporating image and metadata verification alongside text classification, as fake news is often accompanied by manipulated visual assets.
2. **Real-Time Detection**: Optimizing the transformer models (via quantization or distillation into DistilBERT) to allow real-time browser extension validation.
3. **Graph Neural Networks (GNNs)**: Analyzing user interaction and dissemination networks to identify fake news based on how it spreads rather than its content alone.
