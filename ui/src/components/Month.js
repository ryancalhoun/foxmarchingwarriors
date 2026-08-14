class Month {
  constructor(d) {
    this.today = new Date();
    this.date = new Date(d);
  }

  name() {
    return this.date.toLocaleString('default', {month: 'long'});
  }

  first() {
    const d = new Date(this.date);
    d.setDate(1);
    return d;
  }

  last() {
    const d = new Date(this.date);
    d.setMonth(d.getMonth() + 1);
    d.setDate(0);
    return d; 
  }

  month() {
    return this.date.getMonth() + 1;
  }

  year() {
    return this.date.getYear();
  }

  isToday(d) {
    return this.isCurrentMonth(d) && this.today.getDate() == d.getDate();
  }

  isCurrentMonth(d) {
    return this.today.getMonth() == d.getMonth();
  }

  isPast(d) {
    if(this.today.getYear() < d.getYear())
      return true;

    if(this.today.getMonth() < d.getMonth())
      return true;

    return this.today.getDate() < d.getDate();
  }

  getLastSunday() {
        
  }
}
