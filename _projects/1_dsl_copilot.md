---
layout: page
title: Domain Specific Language Copilot
description: Generative AI tool that automatically writes Standard Verification Rule Format (SVRF) language code from natural language prompts.
importance: 1
category: work
related_publications: true
---

This project involved building a specialized Generative AI copilot to accelerate semiconductor physical verification rule development. We trained/fine-tuned and prompt-engineered LLMs to understand SVRF syntax and constraints, wrapping the backend in a Model Context Protocol (MCP) framework to allow agentic tool use and custom validation commands.

### Key Highlights
- **Natural Language to SVRF**: Integrated a web interface and IDE extension that allows design engineers to describe verification rules in plain text and receive complete SVRF decks.
- **LangChain & Agentic Reasoning**: Implemented multi-step reasoning agents that parse input specs, retrieve matching SVRF templates, generate candidate code, and call compiler tools to validate syntax.
- **Impact**: Reduced verification rule development cycles by approximately 40% at Siemens DI SW EDA.
