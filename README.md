# Medical Image Translation Metrics

**Bộ chỉ số đánh giá ảnh y khoa sau chuyển đổi (Medical Image Translation)**

README này giới thiệu cách tính các chỉ số MAE, MSE, PSNR và SSIM giữa ảnh tham chiếu (`actual`) và ảnh được mô hình tạo ra (`predicted`). Đây là các chỉ số định lượng cơ bản cho bài toán image-to-image translation, chẳng hạn CT-to-MRI hoặc MRI-to-CT.

This README explains how to compute MAE, MSE, PSNR, and SSIM between a reference image (`actual`) and a model-generated image (`predicted`). These are basic quantitative metrics for image-to-image translation tasks such as CT-to-MRI or MRI-to-CT.

> **Lưu ý / Note:** Các chỉ số này đo độ giống nhau ở mức pixel/cấu trúc. Chúng không tự xác nhận ảnh tổng hợp an toàn về lâm sàng, bảo toàn tổn thương, hay phù hợp cho chẩn đoán.
> These metrics measure pixel-level or structural similarity. They do not establish clinical safety, lesion preservation, or diagnostic suitability.

## Metrics

| Metric | Ý nghĩa | Meaning | Hướng tốt hơn / Better |
|---|---|---|---|
| **MAE** | Sai số tuyệt đối trung bình giữa các pixel; diễn giải theo đơn vị cường độ ảnh. | Mean absolute pixel error; interpretable in the image intensity units. | Thấp hơn / Lower |
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

## Usage / Cách dùng

Hai ảnh đầu vào phải là ảnh xám 2D, cùng kích thước, và đã được chuẩn hóa về `[0, 1]`.

Both inputs must be 2D grayscale images, have the same shape, and be normalized to `[0, 1]`.

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

## Important notes / Một vài lưu ý

- **Shape và số chiều / Shape and dimensions:** Code chỉ nhận ảnh xám 2D `[H, W]`; `actual` và `predicted` phải có cùng shape. Code này chưa hỗ trợ ảnh 3D/volume.
  
- **Chuẩn hóa và data range / Normalization and data range:** Code hiện giả định cả hai ảnh dùng cùng thang `[0, 1]` (`PSNR` dùng mức đỉnh `1.0`, SSIM dùng `data_range=1.0`). Không chuẩn hóa riêng từng ảnh. Nếu dùng thang `[0, 255]`, phải đổi cả mức đỉnh PSNR thành `255` và SSIM `data_range=255`.
  
- **PSNR:** PSNR được tính từ MSE: `10 * log10(L**2 / MSE)`, trong đó `L` là mức cường độ đỉnh (`1` cho `[0, 1]`, `255` cho `[0, 255]`). Với code hiện tại, công thức là `10 * log10(1 / MSE)`. MSE càng thấp thì PSNR càng cao; nếu hai ảnh giống hệt nhau, MSE bằng `0` và PSNR là `inf`.
  
- **Kích thước SSIM / SSIM window:** `structural_similarity` mặc định dùng cửa sổ 7×7; mỗi chiều ảnh cần ít nhất 7 pixel. Ảnh nhỏ hơn cần `win_size` lẻ nhỏ hơn.
  
- **So sánh y khoa / Medical image evaluation:** Căn chỉnh hai ảnh trước khi so sánh và dùng cùng preprocessing. Metric toàn ảnh có thể bỏ sót thay đổi nhỏ ở tổn thương hoặc cơ quan; cân nhắc đánh giá thêm theo ROI.

## Interpreting results / Diễn giải kết quả

Không có ngưỡng MAE, MSE, PSNR hay SSIM phổ quát để kết luận mô hình tốt cho mọi phương thức ảnh y khoa. Giá trị phụ thuộc vào modality, chuẩn hóa, giải phẫu, quy trình đăng ký và mục tiêu ứng dụng. So sánh các mô hình trên cùng dữ liệu và pipeline, đồng thời xem ảnh trực quan và đánh giá các vùng quan trọng.

There are no universal MAE, MSE, PSNR, or SSIM thresholds that establish a model as good for every medical imaging modality. Values depend on modality, scaling, anatomy, registration, and the intended use. Compare models on the same data and pipeline, and inspect images and clinically important regions alongside the scores.

## License / Giấy phép

Chọn và thêm giấy phép phù hợp với dự án trước khi phát hành công khai.

Choose and add a license appropriate for your project before public release.
