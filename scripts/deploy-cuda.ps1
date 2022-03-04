#!/usr/bin/env pwsh

$url = 'https://developer.download.nvidia.com/compute/cuda/11.6.1/network_installers/cuda_11.6.1_windows_network.exe'

$CudaFeatures = 'nvcc_11.6 cuobjdump_11.6 nvprune_11.6 cupti_11.6 memcheck_11.6 nvdisasm_11.6 nvprof_11.6 ' + `
 'visual_studio_integration_11.6 visual_profiler_11.6 visual_profiler_11.6 cublas_11.6 cublas_dev_11.6 ' + `
 'cudart_11.6 cufft_11.6 cufft_dev_11.6 curand_11.6 curand_dev_11.6 cusolver_11.6 cusolver_dev_11.6 ' + `
 'cusparse_11.6 cusparse_dev_11.6 npp_11.6 npp_dev_11.6 nvrtc_11.6 nvrtc_dev_11.6 nvml_dev_11.6 ' + `
 'occupancy_calculator_11.6 '

try {
  Write-Host 'Downloading CUDA...'
  Invoke-WebRequest -Uri $url -OutFile "cuda_11.6.1_windows_network.exe"
  Write-Host 'Installing CUDA...'
  $proc = Start-Process -PassThru -FilePath "./cuda_11.6.1_windows_network.exe" -ArgumentList @('-s ' + $CudaFeatures)
  $proc.WaitForExit()
  $exitCode = $proc.ExitCode
  if ($exitCode -eq 0) {
    Write-Host 'Installation successful!'
  }
  else {
    Throw "Installation failed! Exited with $exitCode."
  }
}
catch {
  Throw "Failed to install CUDA! $($_.Exception.Message)"
}
