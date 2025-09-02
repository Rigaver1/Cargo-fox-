import { createSlice } from '@reduxjs/toolkit';

const messagesSlice = createSlice({
  name: 'messages',
  initialState: { list: [], current: null },
  reducers: {
    setMessages(state, action) {
      state.list = action.payload;
    },
    setCurrentMessage(state, action) {
      state.current = action.payload;
    },
  },
});

export const { setMessages, setCurrentMessage } = messagesSlice.actions;
export default messagesSlice.reducer;
