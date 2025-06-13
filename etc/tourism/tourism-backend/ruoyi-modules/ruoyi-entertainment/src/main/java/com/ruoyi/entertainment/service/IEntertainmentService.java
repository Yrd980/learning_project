package com.ruoyi.entertainment.service;

import java.util.List;
import com.ruoyi.entertainment.domain.Entertainment;

/**
 * 娱乐信息Service接口
 * 
 * @author ningf
 * @date 2024-07-09
 */
public interface IEntertainmentService 
{
    /**
     * 查询娱乐信息
     * 
     * @param id 娱乐信息主键
     * @return 娱乐信息
     */
    public Entertainment selectEntertainmentById(Long id);

    /**
     * 查询娱乐信息列表
     * 
     * @param entertainment 娱乐信息
     * @return 娱乐信息集合
     */
    public List<Entertainment> selectEntertainmentList(Entertainment entertainment);

    /**
     * 新增娱乐信息
     * 
     * @param entertainment 娱乐信息
     * @return 结果
     */
    public int insertEntertainment(Entertainment entertainment);

    /**
     * 修改娱乐信息
     * 
     * @param entertainment 娱乐信息
     * @return 结果
     */
    public int updateEntertainment(Entertainment entertainment);

    /**
     * 批量删除娱乐信息
     * 
     * @param ids 需要删除的娱乐信息主键集合
     * @return 结果
     */
    public int deleteEntertainmentByIds(Long[] ids);

    /**
     * 删除娱乐信息信息
     * 
     * @param id 娱乐信息主键
     * @return 结果
     */
    public int deleteEntertainmentById(Long id);
}
