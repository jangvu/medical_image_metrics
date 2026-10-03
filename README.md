# Medical Image Translation Metrics

**Bộ chỉ số đánh giá ảnh y khoa sau chuyển đổi (Medical Image Translation)**

README này giới thiệu cách tính các chỉ số MAE, MSE, PSNR và SSIM giữa ảnh tham chiếu (`actual`) và ảnh được mô hình tạo ra (`predicted`). Đây là các chỉ số định lượng cơ bản cho bài toán image-to-image translation, chẳng hạn CT-to-MRI hoặc MRI-to-CT.

This README explains how to compute MAE, MSE, PSNR, and SSIM between a reference image (`actual`) and a model-generated image (`predicted`). These are basic quantitative metrics for image-to-image translation tasks such as CT-to-MRI or MRI-to-CT.

> **Lưu ý / Note:** Các chỉ số này đo độ giống nhau ở mức pixel/cấu trúc. Chúng không tự xác nhận ảnh tổng hợp an toàn về lâm sàng, bảo toàn tổn thương, hay phù hợp cho chẩn đoán.
> These metrics measure pixel-level or structural similarity. They do not establish clinical safety, lesion preservation, or diagnostic suitability.

## Metrics

| Metric | Ý nghĩa (Tiếng Việt) | Meaning (English) | Hướng tốt hơn / Better |
|---|---|---|---|
| **MAE** | Sai số tuyệt đối trung bình giữa các pixel; dễ diễn giải theo đơn vị cường độ ảnh. | Mean absolute pixel error; interpretable in the image intensity units. | Thấp hơn / Lower |
| **MSE** | Trung bình bình phương sai số; phạt mạnh các sai số lớn. | Mean squared pixel error; penalizes larger errors more heavily. | Thấp hơn / Lower |
| **PSNR (dB)** | Tỷ số tín hiệu trên nhiễu đỉnh, được tính từ MSE và mức cường độ pixel tối đa. | Peak signal-to-noise ratio, computed from MSE and the maximum pixel intensity. | Cao hơn / Higher |
| **SSIM** | So sánh độ sáng, độ tương phản và cấu trúc cục bộ giữa hai ảnh. | Compares local luminance, contrast, and structure between images. | Gần 1 hơn / Closer to 1 |

- Nếu hai ảnh giống hệt nhau, MAE và MSE bằng `0`, SSIM thường bằng `1`, còn PSNR là `inf`.
- If the images are identical, MAE and MSE are `0`, SSIM is typically `1`, and PSNR is `inf`.
- PSNR trong code giả định dữ liệu ảnh nằm trong `[0, 1]`. `data_range=1.0` trong SSIM cũng đưa ra giả định tương tự.
- The PSNR formula in this code assumes image values are in `[0, 1]`. SSIM's `data_range=1.0` makes the same assumption.

## Requirements / Cài đặt

Python 3.9+ (recommended) / Python 3.9 trở lên (khuyến nghị)

```bash
pip install numpy scikit-image
```

## Code

```python
import numpy as np
from skimage.metrics import structural_similarity


def my_metrics(actual, predicted):
    actual = np.asarray(actual, dtype=np.float64)
    predicted = np.asarray(predicted, dtype=np.float64)

    if actual.ndim != 2 or actual.shape != predicted.shape:
        raise ValueError("Hai ảnh phải cùng shape [H, W]")

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
```

## Usage / Cách dùng

Hai ảnh đầu vào phải là ảnh xám 2D, cùng kích thước, và đã được chuẩn hóa về `[0, 1]`.

Both inputs must be 2D grayscale images, have the same shape, and be normalized to `[0, 1]`.

```python
import numpy as np
from my_metrics import my_metrics

actual = np.random.rand(256, 256)
predicted = np.clip(actual + np.random.normal(0, 0.02, actual.shape), 0, 1)

scores = my_metrics(actual, predicted)
print(scores)
```

Example output / Ví dụ kết quả:

```python
{
    'MAE': 0.0159,
    'MSE': 0.0004,
    'PSNR_dB': 33.9,
    'SSIM': 0.94
}
```

Kết quả trên chỉ để minh họa; nó thay đổi theo dữ liệu đầu vào.

The output above is illustrative; actual values depend on the input images.

## Important considerations for medical images / Lưu ý với ảnh y khoa

1. **Chuẩn hóa nhất quán / Consistent intensity scaling**  
   Đảm bảo ảnh tham chiếu và ảnh dự đoán dùng cùng phép chuẩn hóa, cửa sổ cường độ, và đơn vị. Với dữ liệu không thuộc `[0, 1]`, cần cập nhật `data_range` cho SSIM và mức đỉnh trong công thức PSNR. Với miền cường độ tối đa là `L`, dùng `10 * log10(L**2 / MSE)`.  
   Ensure reference and predicted images use the same normalization, intensity window, and units. For data outside `[0, 1]`, update SSIM's `data_range` and the peak value in PSNR. For maximum intensity range `L`, use `10 * log10(L**2 / MSE)`.

2. **Đăng ký ảnh / Image registration**  
   Ảnh cần được căn chỉnh không gian trước khi so sánh. Sai lệch nhỏ về vị trí có thể làm MAE/MSE/PSNR/SSIM thay đổi đáng kể.  
   Images should be spatially aligned before comparison. Small shifts can substantially affect all four metrics.

3. **SSIM và kích thước ảnh / SSIM and image size**  
   `structural_similarity` mặc định dùng cửa sổ 7×7; mỗi chiều ảnh thường cần ít nhất 7 pixel.  
   `structural_similarity` uses a 7×7 window by default, so each image dimension generally needs to be at least 7 pixels.

4. **Ảnh 2D, lát cắt 3D và volume / 2D images, 3D slices, and volumes**  
   Hàm này chỉ nhận ảnh 2D. Nếu đánh giá volume 3D, hãy xác định rõ cách tổng hợp kết quả theo lát cắt hoặc dùng metric hỗ trợ 3D; không nên xem mỗi lát cắt là một bệnh nhân độc lập.  
   This function accepts only 2D images. For 3D volumes, define how slice scores are aggregated or use a 3D-capable metric; do not treat each slice as an independent patient.

5. **Không chỉ dựa vào metric toàn ảnh / Do not rely only on whole-image scores**  
   Metric toàn ảnh có thể che khuất thay đổi nhỏ nhưng quan trọng như tổn thương hoặc cấu trúc giải phẫu. Nên báo cáo thêm đánh giá theo ROI/organ, kiểm tra bảo toàn tổn thương, và đánh giá của chuyên gia khi phù hợp.  
   Whole-image scores can hide small but important changes to lesions or anatomy. Consider ROI/organ-level evaluation, lesion-preservation checks, and expert review where appropriate.

6. **So sánh công bằng / Fair comparisons**  
   Dùng cùng preprocessing, tập kiểm thử, và quy tắc tổng hợp cho mọi mô hình. Với dữ liệu nhiều bệnh nhân, tính metric theo từng bệnh nhân trước rồi báo cáo phân phối hoặc trung bình theo quy tắc đã nêu; tránh chia lát cắt giữa train và test.  
   Use the same preprocessing, test set, and aggregation rules for every model. For multi-patient data, compute scores per patient and report a clearly defined distribution or average; avoid splitting slices from one patient across train and test.

## Interpreting results / Diễn giải kết quả

Không có ngưỡng MAE, MSE, PSNR hay SSIM phổ quát để kết luận mô hình tốt cho mọi phương thức ảnh y khoa. Giá trị phụ thuộc vào modality, chuẩn hóa, giải phẫu, quy trình đăng ký và mục tiêu ứng dụng. So sánh các mô hình trên cùng dữ liệu và pipeline, đồng thời xem ảnh trực quan và đánh giá các vùng quan trọng.

There are no universal MAE, MSE, PSNR, or SSIM thresholds that establish a model as good for every medical imaging modality. Values depend on modality, scaling, anatomy, registration, and the intended use. Compare models on the same data and pipeline, and inspect images and clinically important regions alongside the scores.

## License / Giấy phép

Chọn và thêm giấy phép phù hợp với dự án trước khi phát hành công khai.

Choose and add a license appropriate for your project before public release.
