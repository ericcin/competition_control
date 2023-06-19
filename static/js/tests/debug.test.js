const { timePrint, checkType } = require('./debug');

test('timePrint prints the message correctly', () => {
  const printedMessage = timePrint('Hello, World!');
  expect(printedMessage).toMatch(/Hello, World!/);
});

test('timePrint includes the place in the message', () => {
  const printedMessage = timePrint('Welcome!', 'Front Desk');
  expect(printedMessage).toMatch(/Front Desk: Welcome!/);
});

test('checkType returns the correct type', () => {
  const result = checkType(42, 'answer', 'Math');
  expect(result).toBe('number');
});
