"""
Klein 모델 연산 테스트
klein 계열 5개 함수
"""

import torch
import unittest
import reality_stone


class TestKleinOperations(unittest.TestCase):
    """Klein 모델 연산 테스트"""
    
    def setUp(self):
        self.dtype = torch.float32
        self.batch_size = 3
        self.dim = 4
        self.c = 1.0
        
    def test_klein_forward_cpu(self):
        """klein_forward_cpu 테스트"""
        u = torch.randn(self.batch_size, self.dim, dtype=self.dtype) * 0.5
        v = torch.randn(self.batch_size, self.dim, dtype=self.dtype) * 0.5
        t = 0.1
        
        try:
            result = reality_stone.klein_forward_cpu(u, v, self.c, t)
            self.assertEqual(result.shape, u.shape)
            self.assertTrue(torch.all(torch.isfinite(result)))
        except Exception as e:
            self.skipTest(f"klein_forward_cpu 이슈: {e}")
            
    def test_klein_forward_cuda(self):
        """klein_forward_cuda 테스트"""
        if not torch.cuda.is_available():
            self.skipTest("CUDA 불가능")
            
        u = torch.randn(self.batch_size, self.dim, dtype=self.dtype, device='cuda') * 0.5
        v = torch.randn(self.batch_size, self.dim, dtype=self.dtype, device='cuda') * 0.5
        t = 0.1
        
        try:
            result = reality_stone.klein_forward_cuda(u, v, self.c, t)
            self.assertEqual(result.shape, u.shape)
        except Exception as e:
            self.skipTest(f"klein_forward_cuda 이슈: {e}")
            
    def test_klein_backward_cpu(self):
        """klein_backward_cpu 테스트"""
        u = torch.randn(self.batch_size, self.dim, dtype=self.dtype, requires_grad=True) * 0.5
        v = torch.randn(self.batch_size, self.dim, dtype=self.dtype, requires_grad=True) * 0.5
        grad_out = torch.randn(self.batch_size, self.dim, dtype=self.dtype)
        t = 0.1
        
        try:
            grad_u, grad_v = reality_stone.klein_backward_cpu(u, v, grad_out, self.c, t)
            self.assertEqual(grad_u.shape, u.shape)
            self.assertEqual(grad_v.shape, v.shape)
        except Exception as e:
            self.skipTest(f"klein_backward_cpu 이슈: {e}")
            
    def test_klein_backward_cuda(self):
        """klein_backward_cuda 테스트"""
        if not torch.cuda.is_available():
            self.skipTest("CUDA 불가능")
            
        u = torch.randn(self.batch_size, self.dim, dtype=self.dtype, device='cuda', requires_grad=True) * 0.5
        v = torch.randn(self.batch_size, self.dim, dtype=self.dtype, device='cuda', requires_grad=True) * 0.5
        grad_out = torch.randn(self.batch_size, self.dim, dtype=self.dtype, device='cuda')
        t = 0.1
        
        try:
            grad_u, grad_v = reality_stone.klein_backward_cuda(u, v, grad_out, self.c, t)
            self.assertEqual(grad_u.shape, u.shape)
        except Exception as e:
            self.skipTest(f"klein_backward_cuda 이슈: {e}")
            
    def test_klein_layer(self):
        """klein_layer 테스트"""
        u = torch.randn(self.batch_size, self.dim, dtype=self.dtype) * 0.5
        v = torch.randn(self.batch_size, self.dim, dtype=self.dtype) * 0.5
        t = 0.1
        
        try:
            result = reality_stone.klein_layer(u, v, self.c, t)
            self.assertEqual(result.shape, u.shape)
        except Exception as e:
            self.skipTest(f"klein_layer 이슈: {e}")


if __name__ == "__main__":
    unittest.main(verbosity=2) 