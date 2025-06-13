package com.ruoyi.entertainment.service.impl;

import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.entertainment.mapper.ReviewsMapper;
import com.ruoyi.entertainment.domain.Reviews;
import com.ruoyi.entertainment.service.IReviewsService;

/**
 * 餐饮娱乐评价Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-15
 */
@Service
public class ReviewsServiceImpl implements IReviewsService 
{
    @Autowired
    private ReviewsMapper reviewsMapper;

    /**
     * 查询餐饮娱乐评价
     * 
     * @param id 餐饮娱乐评价主键
     * @return 餐饮娱乐评价
     */
    @Override
    public Reviews selectReviewsById(Long id)
    {
        return reviewsMapper.selectReviewsById(id);
    }

    /**
     * 查询餐饮娱乐评价列表
     * 
     * @param reviews 餐饮娱乐评价
     * @return 餐饮娱乐评价
     */
    @Override
    public List<Reviews> selectReviewsList(Reviews reviews)
    {
        return reviewsMapper.selectReviewsList(reviews);
    }

    /**
     * 新增餐饮娱乐评价
     * 
     * @param reviews 餐饮娱乐评价
     * @return 结果
     */
    @Override
    public int insertReviews(Reviews reviews)
    {
        return reviewsMapper.insertReviews(reviews);
    }

    /**
     * 修改餐饮娱乐评价
     * 
     * @param reviews 餐饮娱乐评价
     * @return 结果
     */
    @Override
    public int updateReviews(Reviews reviews)
    {
        return reviewsMapper.updateReviews(reviews);
    }

    /**
     * 批量删除餐饮娱乐评价
     * 
     * @param ids 需要删除的餐饮娱乐评价主键
     * @return 结果
     */
    @Override
    public int deleteReviewsByIds(Long[] ids)
    {
        return reviewsMapper.deleteReviewsByIds(ids);
    }

    /**
     * 删除餐饮娱乐评价信息
     * 
     * @param id 餐饮娱乐评价主键
     * @return 结果
     */
    @Override
    public int deleteReviewsById(Long id)
    {
        return reviewsMapper.deleteReviewsById(id);
    }
}
