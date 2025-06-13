package com.ruoyi.entertainment.mapper;

import java.util.List;
import com.ruoyi.entertainment.domain.Reviews;

/**
 * 餐饮娱乐评价Mapper接口
 * 
 * @author ningf
 * @date 2024-07-15
 */
public interface ReviewsMapper 
{
    /**
     * 查询餐饮娱乐评价
     * 
     * @param id 餐饮娱乐评价主键
     * @return 餐饮娱乐评价
     */
    public Reviews selectReviewsById(Long id);

    /**
     * 查询餐饮娱乐评价列表
     * 
     * @param reviews 餐饮娱乐评价
     * @return 餐饮娱乐评价集合
     */
    public List<Reviews> selectReviewsList(Reviews reviews);

    /**
     * 新增餐饮娱乐评价
     * 
     * @param reviews 餐饮娱乐评价
     * @return 结果
     */
    public int insertReviews(Reviews reviews);

    /**
     * 修改餐饮娱乐评价
     * 
     * @param reviews 餐饮娱乐评价
     * @return 结果
     */
    public int updateReviews(Reviews reviews);

    /**
     * 删除餐饮娱乐评价
     * 
     * @param id 餐饮娱乐评价主键
     * @return 结果
     */
    public int deleteReviewsById(Long id);

    /**
     * 批量删除餐饮娱乐评价
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteReviewsByIds(Long[] ids);
}
