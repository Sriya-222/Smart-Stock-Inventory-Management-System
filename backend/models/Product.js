const mongoose = require('mongoose');

const ProductSchema = new mongoose.Schema({
  name: { type: String, required: true },
  description: { type: String, required: true },
  price: { type: Number, required: true },
  stock: { type: Number, required: true, default: 0 },
  category: { type: String, default: 'General' },
  imageUrl: { type: String, default: 'https://placehold.co/400x300' },
  // Smart Inventory Options
  sku: { type: String, required: false },
  costPrice: { type: Number, required: false, default: 0 },
  minLevel: { type: Number, required: false, default: 10 },
  reorderPoint: { type: Number, required: false, default: 20 },
}, { timestamps: true });

module.exports = mongoose.model('Product', ProductSchema);
