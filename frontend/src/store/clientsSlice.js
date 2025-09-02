import { createSlice } from '@reduxjs/toolkit';

const clientsSlice = createSlice({
  name: 'clients',
  initialState: { list: [], current: null },
  reducers: {
    setClients(state, action) {
      state.list = action.payload;
    },
    setCurrentClient(state, action) {
      state.current = action.payload;
    },
  },
});

export const { setClients, setCurrentClient } = clientsSlice.actions;
export default clientsSlice.reducer;
