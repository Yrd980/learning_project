package com.ruoyi.entertainment.service;

import java.util.List;
import com.ruoyi.entertainment.domain.Diningentertainment;

/**
 * 餐饮娱乐信息Service接口
 * 
 * @author ningf
 * @date 2024-07-08
 */
public interface IDiningentertainmentService 
{
    /**
     * 查询餐饮娱乐信息
     * 
     * @param id 餐饮娱乐信息主键
     * @return 餐饮娱乐信息
     */
    public Diningentertainment selectDiningentertainmentById(Long id);

    /**
     * 查询餐饮娱乐信息列表
     * 
     * @param diningentertainment 餐饮娱乐信息
     * @return 餐饮娱乐信息集合
     */
    public List<Diningentertainment> selectDiningentertainmentList(Diningentertainment diningentertainment);

    /**
     * 新增餐饮娱乐信息
     * 
     * @param diningentertainment 餐饮娱乐信息
     * @return 结果
     */
    public int insertDiningentertainment(Diningentertainment diningentertainment);

    /**
     * 修改餐饮娱乐信息
     * 
     * @param diningentertainment 餐饮娱乐信息
     * @return 结果
     */
    public int updateDiningentertainment(Diningentertainment diningentertainment);

    /**
     * 批量删除餐饮娱乐信息
     * 
     * @param ids 需要删除的餐饮娱乐信息主键集合
     * @return 结果
     */
    public int deleteDiningentertainmentByIds(Long[] ids);

    /**
     * 删除餐饮娱乐信息信息
     * 
     * @param id 餐饮娱乐信息主键
     * @return 结果
     */
    public int deleteDiningentertainmentById(Long id);
}
