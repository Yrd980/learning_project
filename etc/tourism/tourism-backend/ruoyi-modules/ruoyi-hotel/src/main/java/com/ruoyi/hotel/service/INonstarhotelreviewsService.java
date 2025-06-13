package com.ruoyi.hotel.service;

import java.util.List;
import com.ruoyi.hotel.domain.Nonstarhotelreviews;

/**
 * 非星级酒店评价Service接口
 * 
 * @author ningf
 * @date 2024-07-15
 */
public interface INonstarhotelreviewsService 
{
    /**
     * 查询非星级酒店评价
     * 
     * @param id 非星级酒店评价主键
     * @return 非星级酒店评价
     */
    public Nonstarhotelreviews selectNonstarhotelreviewsById(Long id);

    /**
     * 查询非星级酒店评价列表
     * 
     * @param nonstarhotelreviews 非星级酒店评价
     * @return 非星级酒店评价集合
     */
    public List<Nonstarhotelreviews> selectNonstarhotelreviewsList(Nonstarhotelreviews nonstarhotelreviews);

    /**
     * 新增非星级酒店评价
     * 
     * @param nonstarhotelreviews 非星级酒店评价
     * @return 结果
     */
    public int insertNonstarhotelreviews(Nonstarhotelreviews nonstarhotelreviews);

    /**
     * 修改非星级酒店评价
     * 
     * @param nonstarhotelreviews 非星级酒店评价
     * @return 结果
     */
    public int updateNonstarhotelreviews(Nonstarhotelreviews nonstarhotelreviews);

    /**
     * 批量删除非星级酒店评价
     * 
     * @param ids 需要删除的非星级酒店评价主键集合
     * @return 结果
     */
    public int deleteNonstarhotelreviewsByIds(Long[] ids);

    /**
     * 删除非星级酒店评价信息
     * 
     * @param id 非星级酒店评价主键
     * @return 结果
     */
    public int deleteNonstarhotelreviewsById(Long id);
}
