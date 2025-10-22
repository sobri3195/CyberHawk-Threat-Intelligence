import express from 'express';
import { 
  getRecentThreats, 
  getThreatsByLevel,
  searchThreats 
} from '../controllers/threatsController.js';

const router = express.Router();

router.get('/recent', getRecentThreats);
router.get('/level/:level', getThreatsByLevel);
router.post('/search', searchThreats);

export default router;
