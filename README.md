# Project 1 - AI Chatbot with Conversation Memory

An AI chatbot/agent built using FastAPI and Google Gemini API with automatic tool calling, persistent conversation memory, and error handling.

## Features

- FastAPI REST API
- Google Gemini API integration
- Automatic function/tool calling
- Weather tool
- Addition tool
- Multiplication tool
- Conversation memory using SQLite
- Memory-aware Gemini responses
- Normal conversation handling
- Unsupported request handling
- Error handling for external API failures
- Pydantic request/response validation
- Environment variable based API key
- Swagger API testing

## Tech Stack

- Python
- FastAPI
- Google Gemini API
- Pydantic
- SQLite
- python-dotenv
- Requests

## Available Tools

### Weather

Gets the current weather information for a city.

### Addition

Adds two numbers.

### Multiplication

Multiplies two numbers.

Gemini automatically decides when a tool is required and calls the appropriate function.

## Conversation Memory

The chatbot stores conversations in a local SQLite database.

Previous relevant conversations can be provided to Gemini as context so the agent can answer memory-related questions.

`memory.db` is kept local and is not committed to GitHub.

## API

### POST `/chat`

Send a user prompt to the AI agent.

Example request:

```json
{
  "prompt": "What is the weather in Mumbai?"
}