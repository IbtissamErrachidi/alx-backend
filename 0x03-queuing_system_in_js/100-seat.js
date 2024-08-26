import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';
import express from 'express';

const client = redis.createClient();
const reserveSeat = promisify(client.set).bind(client);
const getAsync = promisify(client.get).bind(client);

const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return parseInt(seats, 10);
};

let reservationEnabled = true;
const queue = kue.createQueue();
const app = express();
const port = 1245;

// Initialiser le nombre de sièges disponibles à 50
reserveSeat('available_seats', 50);

app.get('/available_seats', async (req, res) => {
  const numberOfAvailableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: "Reservation are blocked" });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (!err) {
      return res.json({ status: "Reservation in process" });
    } else {
      return res.json({ status: "Reservation failed" });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

app.get('/process', async (req, res) => {
  res.json({ status: "Queue processing" });

  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    const seatsLeft = parseInt(availableSeats, 10);

    if (seatsLeft > 0) {
      await reserveSeat('available_seats', seatsLeft - 1);

      if (seatsLeft - 1 === 0) {
        reservationEnabled = false;
      }

      done();
    } else {
      done(new Error('Not enough seats available'));
    }
  });
});

app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

