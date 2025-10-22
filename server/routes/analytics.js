import express from 'express';
import { getSentimentAnalysis, getTrendAnalysis } from '../controllers/analyticsController.js';

const router = express.Router();

router.get('/sentiment', getSentimentAnalysis);
router.get('/trends', getTrendAnalysis);

export default router;
