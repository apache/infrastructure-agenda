export const CLOCK_INCREMENT = 'CLOCK_INCREMENT';
export const CLOCK_DECREMENT = 'CLOCK_DECREMENT';
export const POST_AGENDA = 'POST_AGENDA';
export const POST_SERVER = 'POST_SERVER';
export const HISTORICAL_COMMENTS = "HISTORICAL_COMMENTS";
export const RESPONSES="RESPONSES";

export const clockIncrement = () => ({ type: CLOCK_INCREMENT });
export const clockDecrement = () => ({ type: CLOCK_DECREMENT });

export const postAgenda = (index) => ({ type: POST_AGENDA, index });
export const postServer = (server) => ({ type: POST_SERVER, server });

export const historicalComments = (comments) => ({ type: HISTORICAL_COMMENTS, comments});

export const responses = (messages) => ({ type: RESPONSES, messages })