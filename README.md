# Tarot MCP Server

A Model Context Protocol (MCP) server that brings tarot card readings to AI assistants like Claude. Draw cards, perform spreads, and explore card meanings directly from your conversations.

In my opinion, tarot can't predict the future, and this project doesn't pretend it can. It can however act as a tool for introspection — the cards' symbolism works as prompts for self-reflection, similar to how tarot is sometimes used in therapeutic settings.

To get access to this tool, you can either build your own or use my server (http://124.222.93.49:7878/tarot_mcp), however my server does not have a domain nor lisense which may be block by some chatbot client.

## Features

- **Full 78-card deck** — All 22 Major Arcana and 56 Minor Arcana cards, with upright and reversed meanings
- **Random card draws** — Draw a single card or multiple cards with true shuffling
- **Classic spreads** — Support for common spreads such as single card, three-card (past / present / future), cyberpunk 2077 cross four, and Celtic Cross
- **Card lookup** — Query the detailed meaning, symbolism, and keywords of any card

## Installation

Clone the repository:

```bash
git clone https://github.com/hwfish/tarot_mcp_server.git
cd tarot_mcp_server
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Example Prompts

Once connected, try asking your AI assistant:

- "Draw a tarot card for me."
- "Do a three-card spread about my career."
- "What does The Tower mean when reversed?"

## Available Tools

```
|        Tool        |                        Description                        |
|--------------------|-----------------------------------------------------------|
|     `draw_card`    | Draw one or more random cards from the deck               |
| `get_card_meaning` | Look up the meaning of a specific card                    |
|  `perform_spread`  | Perform a tarot spread (single, three-card, Celtic Cross) |
```