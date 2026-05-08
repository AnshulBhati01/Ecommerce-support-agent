AI Agents for High‑Volume Customer Support 
This document contains three case studies focused on designing and understanding AI 
Agents for High‑Volume Customer Support.  
Instructions  
Please complete 3 case studies as per the guidelines below. Upload your completed case 
study solutions to SharePoint and share the link in the form:  Case Study Solution 
Submission – Fill out form 
Case Study 1: AI Customer Support Agent for E‑Commerce Platforms 
Executive Summary 
E‑commerce platforms receive extremely high volumes of customer queries related to 
orders, returns, refunds, and delivery tracking—especially during peak sales periods. An AI 
Customer Support Agent is introduced to handle these interactions efficiently. 
Business Problem 
Support teams struggle to manage repetitive customer queries during traffic spikes, leading 
to long wait times, increased operational costs, and reduced customer satisfaction. 
Objectives 
• Automate high‑frequency customer support queries 
• Reduce response times during peak loads 
• Improve first‑contact resolution 
• Ensure smooth escalation to human agents 
Solution Overview 
The AI agent uses an LLM with Retrieval‑Augmented Generation (RAG) to answer FAQs, 
retrieve order information, and initiate simple workflows such as returns. 
Workflow 
1. Customer submits a query via chat 
2. Agent identifies intent and key entities 
3. Relevant knowledge or order data is retrieved 
4. Response is generated or action is triggered 
5. Complex issues are escalated with context 
Sample Q&A 
Q: Where is my order? It was supposed to arrive yesterday. 
A: Your order is currently delayed due to logistics issues and is expected to arrive 
tomorrow. Would you like to receive delivery updates? 
Internal - General Use 
Q: I want to return the item I received. 
A: I can help you initiate a return. Please share your order ID to proceed. 
Case Study 2: AI Customer Support Agent for Banking using GitHub Copilot 
Executive Summary 
Banks handle thousands of daily customer queries related to accounts, transactions, and 
cards. An AI Customer Support Agent is developed to manage this volume, with GitHub 
Copilot accelerating the development of secure backend services. 
Business Problem 
Manual handling of repetitive banking queries results in high call‑center costs and slower 
customer service. 
Objectives 
• Automate Tier‑0 and Tier‑1 banking support queries 
• Maintain compliance and security standards 
• Reduce dependency on human agents 
• Speed up development using AI coding assistance 
Role of GitHub Copilot 
GitHub Copilot assists developers by generating API code, suggesting secure patterns, and 
helping write validation logic and tests for customer support workflows. 
Workflow 
1. Customer initiates a secure chat session 
2. Agent classifies intent and evaluates risk 
3. Knowledge‑based response or validation step is executed 
4. Sensitive requests are escalated if required 
Sample Q&A 
Q: Why is my card transaction still pending? 
A: Pending transactions are temporary holds by merchants and usually complete within a 
few business days. 
Q: My debit card is blocked. 
A: For security reasons, I need to verify your identity before helping you unblock the card or 
escalating this request. 
Internal - General Use 
Case Study 3: AI Customer Support Agent using Google ADK and LangChain 
Executive Summary 
High‑volume enterprise customer support often requires handling complex, multi‑step 
issues. This case study presents a modular AI Customer Support Agent built using Google 
ADK and LangChain. 
Business Problem 
Traditional single‑agent chatbots struggle with scalability, context handling, and complex 
issue resolution. 
Objectives 
• Support large volumes of concurrent conversations 
• Improve accuracy through retrieval‑based responses 
• Enable structured escalation flows 
• Maintain conversation context across sessions 
Role of Google ADK and LangChain 
Google ADK manages agent teams, execution flow, and session state. LangChain enables 
retrieval, tool usage, and reasoning for customer support interactions. 
Workflow 
1. Customer submits a support request 
2. Planner agent routes the request 
3. LangChain retrieves relevant knowledge 
4. Response is generated or escalated 
Sample Q&A 
Q: My application fails every time I try to log in. 
A: I will check known issues and recent incidents related to login failures before suggesting 
next steps. 
Q: This issue is still not resolved. 
A: I am escalating this issue to a support specialist with the full conversation context and 
diagnostics. 
Internal - General Use 
