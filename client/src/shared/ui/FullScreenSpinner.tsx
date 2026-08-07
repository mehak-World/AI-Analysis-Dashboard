// ui/FullScreenSpinner.tsx
import { Spinner } from "./Spinner";

export function FullScreenSpinner() {
  return (
    <div className="flex h-screen w-full items-center justify-center bg-slate-950">
      <Spinner size="lg" />
    </div>
  );
}