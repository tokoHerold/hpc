#!/bin/bash
mkdir -p data

echo "Executing sum_direct..."
./build/sum_direct > data/direct.csv
echo "Executing sum_vector..."
./build/sum_vector > data/vector.csv
echo "Executing sum_direct..."
./build/sum_indirect > data/indirect.csv
echo "Done!"

