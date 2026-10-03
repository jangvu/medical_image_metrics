import numpy as np
from skimage.metrics import structural_similarity


def metrics(actual, predicted):
    actual = np.asarray(actual, dtype=np.float64)
    predicted = np.asarray(predicted, dtype=np.float64)

    if actual.ndim != 2 or actual.shape != predicted.shape:
        raise ValueError("Two images need the same shape [H, W]")

    difference = predicted - actual

    mae = np.mean(np.abs(difference))
    mse = np.mean(difference ** 2)
    psnr = float("inf") if mse == 0 else 10 * np.log10(1.0 / mse)
    ssim = structural_similarity(actual, predicted, data_range=1.0)

    return {
        "MAE": float(mae),
        "MSE": float(mse),
        "PSNR_dB": float(psnr),
        "SSIM": float(ssim),
    }
