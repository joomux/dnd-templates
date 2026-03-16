# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

- **Build**: `npm run build` or `make build` - Build the project for production
- **Lint**: `npm run lint` or `make lint` - Run linting checks
- **Test**: `npm test` or `make test` - Run all tests
- **Run single test**: `npm test -- --grep "test-name"` or `make test-single TEST_NAME=test-name`
- **Start development server**: `npm run dev` or `make serve`

*Note: Update commands based on the actual project configuration (package.json, Makefile, etc.)*

## Architecture

This is a D&D (Dungeons & Dragons) template repository designed to provide a foundation for creating character sheets, campaign management tools, or other D&D-related applications.

**Key Components:**

1. **Core Game Engine** - Handles D&D mechanics, dice rolling, character progression
2. **UI Layer** - React-based components for character sheets, dice rollers, campaign management
3. **Data Layer** - Local storage and potentially cloud sync for character data and campaigns
4. **Template System** - Extensible templates for different D&D editions and homebrew rules

**File Structure:**

- `src/components/` - Reusable UI components
- `src/game/` - Core game mechanics and rules
- `src/templates/` - Character sheet and campaign templates
- `src/utils/` - Utility functions for dice rolling, formatting, etc.

*Note: Update architecture based on the actual codebase structure and conventions.*