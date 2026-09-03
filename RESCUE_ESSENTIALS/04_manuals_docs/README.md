
## Development

### Available Scripts

In the project root, you can run:

- `pnpm dev` - Start all apps in development mode
- `pnpm build` - Build all apps for production
- `pnpm test` - Run test suites
- `pnpm lint` - Run ESLint
- `pnpm typecheck` - Run TypeScript type checking

### Environment Setup

1. Copy `.env.example` to `.env.local`
2. Fill in your Supabase credentials
3. Never commit `.env.local` - it's gitignored for your safety

### Database Setup

The Supabase schema is located in `supabase/migrations/`. To apply migrations:

```bash
# Using Supabase CLI
supabase db push --project-id YOUR_PROJECT_ID

# Or apply manually through Supabase dashboard
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the **GNU AGPL-3.0-or-later** — see the [LICENSE](LICENSE) file for details. Public code, stays public: any deployed fork must also publish its source under AGPL-3.0.

## Security

Please report security vulnerabilities to security@milyfe.os or through our [private reporting process](SECURITY.md).

---
*Built with ❤️ for the MiLyfe community*
