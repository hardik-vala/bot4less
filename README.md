# Install

```
pip install -r deps_py.txt
```

With `virtualenv`,

```
virtualenv .venv && \
    source .venv/bin/activate && \
    pip install -r deps_py.txt
```

# Run

## Personal Macbook Pro

```
source ~/Code/bot4less/.venv/bin/activate && python3 ~/Code/bot4less/python/bot4less.py --chromedriver_path=/usr/local/bin/chromedriver --num_future_booking_days=3 >> ~/Code/bot4less/logs.txt 2>&1
```

(Fit4Less allows booking a maximum of 2 days in advance. But bookings become
available at midnight, ET, and this script will run at 9 pm, PT, so necessarily,
the value here is 3 days.)

## VInn-BackOffice Desktop

```
bot4less.bat
```