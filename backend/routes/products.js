const express = require('express');
const { auth, admin } = require('../middleware/auth');
const Product = require('../models/Product');
const router = express.Router();

// Get all products (public/authenticated)
router.get('/', async (req, res) => {
  try {
    const products = await Product.find().sort({ createdAt: -1 });
    res.json(products);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Add a new product (Admin only)
router.post('/', [auth, admin], async (req, res) => {
  try {
    const newProduct = new Product(req.body);
    const savedProduct = await newProduct.save();
    res.status(201).json(savedProduct);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Delete a product (Admin only)
router.delete('/:id', [auth, admin], async (req, res) => {
  try {
    const product = await Product.findByIdAndDelete(req.params.id);
    if (!product) return res.status(404).json({ message: 'Product not found' });
    res.json({ message: 'Product removed' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Buy a product (User)
router.put('/:id/buy', auth, async (req, res) => {
  try {
    const { quantity } = req.body;
    const parsedQuantity = parseInt(quantity, 10) || 1;
    
    if (parsedQuantity <= 0) return res.status(400).json({ message: 'Invalid quantity' });

    const product = await Product.findById(req.params.id);
    if (!product) return res.status(404).json({ message: 'Product not found' });

    if (product.stock < parsedQuantity) {
      return res.status(400).json({ message: 'Insufficient stock available' });
    }

    product.stock -= parsedQuantity;
    const updatedProduct = await product.save();

    res.json(updatedProduct);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
