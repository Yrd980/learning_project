package com.ruoyi.complaint.mapper;

import java.util.List;
import com.ruoyi.complaint.domain.Handlingresults;

/**
 * 投诉处理结果Mapper接口
 * 
 * @author ningf
 * @date 2024-07-15
 */
public interface HandlingresultsMapper 
{
    /**
     * 查询投诉处理结果
     * 
     * @param id 投诉处理结果主键
     * @return 投诉处理结果
     */
    public Handlingresults selectHandlingresultsById(Long id);

    /**
     * 查询投诉处理结果列表
     * 
     * @param handlingresults 投诉处理结果
     * @return 投诉处理结果集合
     */
    public List<Handlingresults> selectHandlingresultsList(Handlingresults handlingresults);

    /**
     * 新增投诉处理结果
     * 
     * @param handlingresults 投诉处理结果
     * @return 结果
     */
    public int insertHandlingresults(Handlingresults handlingresults);

    public int insertHandlingresultsbyId(Long[] ids);

    /**
     * 修改投诉处理结果
     * 
     * @param handlingresults 投诉处理结果
     * @return 结果
     */
    public int updateHandlingresults(Handlingresults handlingresults);

    /**
     * 删除投诉处理结果
     * 
     * @param id 投诉处理结果主键
     * @return 结果
     */
    public int deleteHandlingresultsById(Long id);

    /**
     * 批量删除投诉处理结果
     * 
     * @param ids 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteHandlingresultsByIds(Long[] ids);
}
