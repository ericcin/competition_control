const timePrint = (message, place, variableName) => {
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    const timestamp = new Date().toLocaleString('en-US', { timeZone: timezone }).slice(0, 19).replace('T', ' ');
    const baseMessage = variableName ? `${variableName} = ${message}` : `${message}`
    const filledMessage = place ? `(${timezone}) ${timestamp}: ${place}: ${baseMessage}` : `${timestamp}: ${baseMessage}`;
    console.log(filledMessage);
    return filledMessage;
};

function checkType(variable, variableName = 'data', place) {
    const type = typeof variable;
    const message = `typeof(${variableName}) = ${type}`;
    timePrint(message, place);
    if (type === 'object') {
        console.dir(variable);
    }

    return type;
}

function scrutinize(variable, variableName = 'data', place) {
    return [timePrint(variable, place, variableName), checkType(variable, variableName, place)]
}