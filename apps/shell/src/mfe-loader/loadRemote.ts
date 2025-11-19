/**
 * Helper function to load remote modules via Module Federation
 * Vite Module Federation handles the container loading automatically
 * The format should be: 'remote_name/./module_name' where module_name matches the expose key
 */
export default async function loadRemote(remoteName: string, moduleName: string): Promise<any> {
  try {
    // Ensure moduleName starts with './' to match the expose format
    const modulePath = moduleName.startsWith('./') 
      ? `${remoteName}/${moduleName}` 
      : `${remoteName}/./${moduleName}`;
    
    // The plugin automatically handles loading the remoteEntry and resolving the module
    const module = await import(/* @vite-ignore */ modulePath);
    
    // Return the default export or the module itself
    if (module.default) {
      return { default: module.default };
    }
    
    // If no default export, return the module as default
    return { default: module };
  } catch (error) {
    const remotes = (window as any).__remotes__;
    const remoteUrl = remotes?.[remoteName] || `${remoteName}/${moduleName}`;
    console.error(`Error loading remote module ${remoteName}/${moduleName} from ${remoteUrl}:`, error);
    throw new Error(
      `Failed to load remote module ${remoteName}/${moduleName}. Make sure the remote is running and accessible at ${remoteUrl}.`
    );
  }
}

