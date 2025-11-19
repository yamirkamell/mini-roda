import React, { Suspense, Component, ErrorInfo, ReactNode } from 'react';
import loadRemote from './loadRemote';

interface RemoteWrapperProps {
  system: string;
  module: string;
  fallback?: ReactNode;
}

interface RemoteWrapperState {
  hasError: boolean;
  error?: Error;
}

class RemoteErrorBoundary extends Component<
  { children: ReactNode },
  RemoteWrapperState
> {
  constructor(props: { children: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): RemoteWrapperState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Remote module error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-boundary">
          <h3>Error al cargar el módulo</h3>
          <p>{this.state.error?.message || 'Error desconocido'}</p>
          <button
            onClick={() => this.setState({ hasError: false, error: undefined })}
          >
            Reintentar
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}


export default function RemoteWrapper({
  system,
  module,
  fallback = <div className="loading">Cargando módulo...</div>,
}: RemoteWrapperProps) {
  // Create the lazy component using loadRemote
  const Component = React.lazy(() => loadRemote(system, module));

  return (
    <RemoteErrorBoundary>
      <Suspense fallback={fallback}>
        <Component />
      </Suspense>
    </RemoteErrorBoundary>
  );
}

