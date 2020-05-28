const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
let month = document.querySelector('#renderRange');
month.innerHTML = dateFns.format(Date.now(), 'MMMM');

var cal = new tui.Calendar('#calendar', {
    defaultView: 'month',
    taskView: true,
});

cal.createSchedules([
    {
        id: '1',
        calendarId: '1',
        title: 'test',
        category: 'time',
        start: '2020-05-18T22:30:00+09:00',
        end: '2020-05-23T02:30:00+09:00'
    }
])

function prev() {
    let currentMonth = month.innerHTML;
    let index = months.indexOf(currentMonth);
    if ( index == 0 ) {
        month.innerHTML = months[11];
    } else {
        month.innerHTML = months[index - 1];
    }
    cal.prev();
}

function next() {
    let currentMonth = month.innerHTML;
    let index = months.indexOf(currentMonth);
    if ( index == 11 ) {
        month.innerHTML = months[0];
    } else {
        month.innerHTML = months[index + 1];
    }
    cal.next();
}