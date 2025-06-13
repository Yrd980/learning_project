package com.ruoyi.hotel.service;

import java.util.List;
import com.ruoyi.hotel.domain.Starhotelreviews;

/**
 * 星级酒店评价Service接口
 * 
 * @author ningf
 * @date 2024-07-15
 */
public interface IStarhotelreviewsService 
{
    /**
     * 查询星级酒店评价
     * 
     * @param id 星级酒店评价主键
     * @return 星级酒店评价
     */
    public Starhotelreviews selectStarhotelreviewsById(Long id);

    /**
     * 查询星级酒店评价列表
     * 
     * @param starhotelreviews 星级酒店评价
     * @return 星级酒店评价集合
     */
    public List<Starhotelreviews> selectStarhotelreviewsList(Starhotelreviews starhotelreviews);

    /**
     * 新增星级酒店评价
     * 
     * @param starhotelreviews 星级酒店评价
     * @return 结果
     */
    public int insertStarhotelreviews(Starhotelreviews starhotelreviews);

    /**
     * 修改星级酒店评价
     * 
     * @param starhotelreviews 星级酒店评价
     * @return 结果
     */
    public int updateStarhotelreviews(Starhotelreviews starhotelreviews);

    /**
     * 批量删除星级酒店评价
     * 
     * @param ids 需要删除的星级酒店评价主键集合
     * @return 结果
     */
    public int deleteStarhotelreviewsByIds(Long[] ids);

    /**
     * 删除星级酒店评价信息
     * 
     * @param id 星级酒店评价主键
     * @return 结果
     */
    public int deleteStarhotelreviewsById(Long id);
}
