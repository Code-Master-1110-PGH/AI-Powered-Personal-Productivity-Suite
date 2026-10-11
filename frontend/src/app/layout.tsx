import type { Metadata } from 'next';
import '@/styles/globals.css';

export const metadata: Metadata = {
  title: 'Synapse OS | AI-Powered Personal Productivity Suite',
  description:
    'Next-generation enterprise productivity platform featuring Smart Resume Reviewer and AI Natural Language Scheduler.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-background text-slate-100 antialiased selection:bg-cyan-500 selection:text-black">
        {/* Ambient Glow Orbs */}
        <div className="fixed inset-0 pointer-events-none overflow-hidden z-0">
          <div className="absolute -top-40 -left-40 w-96 h-96 bg-cyan-500/10 rounded-full blur-[128px]" />
          <div className="absolute top-1/3 -right-40 w-96 h-96 bg-purple-500/10 rounded-full blur-[128px]" />
          <div className="absolute -bottom-40 left-1/3 w-96 h-96 bg-emerald-500/10 rounded-full blur-[128px]" />
          <div className="absolute inset-0 bg-grid-cyber" />
        </div>

        <div className="relative z-10">{children}</div>
      </body>
    </html>
  );
}

