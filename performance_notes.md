# Performance Analysis for Toxic Content Classification API

## Azure VM Configuration
- **Instance Type**: Standard B1ms
- **vCPUs**: 1
- **RAM**: 2 GiB
- **Network**: Standard

## Performance Estimates

### Maximum Concurrent Users
With the current optimized configuration (1 worker, 4 threads, limited concurrency):

- **Single text classification**: ~15-20 concurrent users/second
- **Batch processing (10 texts)**: ~2-3 batch requests/second (~20-30 texts/second)

### Response Time Estimates
- **Single text request**: 400-800ms average
- **Batch request (10 texts)**: 1.5-3 seconds average

### Resource Utilization
- **Memory Usage**:
  - Base FastAPI application: ~100-150MB
  - Transformer model: ~800-1000MB
  - Operating system: ~150-200MB
  - Available for request handling: ~650-950MB

- **CPU Utilization**:
  - Inference operations: ~70-80% CPU
  - Request handling: ~10-15% CPU
  - Background tasks: ~5-10% CPU

## Limiting Factors

1. **Memory Constraints (Primary Bottleneck)**
   - The transformer model requires significant memory
   - Large batch sizes may cause OOM errors

2. **CPU Processing Power**
   - Single vCPU limits parallel processing
   - B1ms has burst capabilities but sustained processing is limited

3. **B-series Burstable Performance**
   - Can handle spikes in traffic by using CPU credits
   - Performance decreases during sustained high load

## Optimization Strategies Implemented

1. **Worker & Thread Reduction**
   - Single worker to avoid context switching overhead
   - Limited thread pool (4 threads) to prevent CPU contention

2. **Memory Management**
   - Added swap file to handle memory peaks
   - Environment variables to limit PyTorch memory fragmentation

3. **Concurrency Control**
   - Limited to 20 concurrent requests
   - Increased keep-alive timeout to reduce connection overhead

## Monitoring Recommendations

For optimal performance monitoring:
1. Track memory usage with Azure Monitor
2. Set up alerts for high CPU utilization (>90%)
3. Monitor response times and failed requests
4. Set up auto-restart if memory usage exceeds 80%

## Scaling Options

If higher throughput is required:
1. **Vertical Scaling**: Upgrade to B2s (2 vCPU, 4 GiB) for 2-3x performance
2. **Implement Queue**: Add Azure Queue Storage for processing requests asynchronously
3. **Caching**: Implement Redis cache for repeated classification requests
