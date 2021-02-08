import React from 'react';

export default function usePersistedState(key, defaultValue) {
  const [state, setState] = React.useState(() => {
    const persistedState = sessionStorage.getItem(key);
    return persistedState ? JSON.parse(persistedState) : defaultValue;
  });
  React.useEffect(() => {
    window.sessionStorage.setItem(key, JSON.stringify(state));
  }, [state, key]);
  return [state, setState];
}
