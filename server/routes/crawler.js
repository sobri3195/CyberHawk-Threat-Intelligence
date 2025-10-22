import express from 'express';
import { startCrawl, getCrawlStatus } from '../controllers/crawlerController.js';

const router = express.Router();

router.post('/start', startCrawl);
router.get('/status', getCrawlStatus);

export default router;
