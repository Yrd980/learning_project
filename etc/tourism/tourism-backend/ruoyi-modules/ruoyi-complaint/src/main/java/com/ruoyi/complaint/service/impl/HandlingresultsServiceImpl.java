package com.ruoyi.complaint.service.impl;

import java.util.List;

import com.ruoyi.complaint.mapper.ComplaintsMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.complaint.mapper.HandlingresultsMapper;
import com.ruoyi.complaint.domain.Handlingresults;
import com.ruoyi.complaint.service.IHandlingresultsService;

/**
 * 投诉处理结果Service业务层处理
 * 
 * @author ningf
 * @date 2024-07-15
 */
@Service
public class HandlingresultsServiceImpl implements IHandlingresultsService 
{
    @Autowired
    private HandlingresultsMapper handlingresultsMapper;

    /**
     * 查询投诉处理结果
     * 
     * @param id 投诉处理结果主键
     * @return 投诉处理结果
     */
    @Override
    public Handlingresults selectHandlingresultsById(Long id)
    {
        return handlingresultsMapper.selectHandlingresultsById(id);
    }

    /**
     * 查询投诉处理结果列表
     * 
     * @param handlingresults 投诉处理结果
     * @return 投诉处理结果
     */
    @Override
    public List<Handlingresults> selectHandlingresultsList(Handlingresults handlingresults)
    {
        return handlingresultsMapper.selectHandlingresultsList(handlingresults);
    }

    /**
     * 新增投诉处理结果
     * 
     * @param handlingresults 投诉处理结果
     * @return 结果
     */
    @Override
    public int insertHandlingresults(Handlingresults handlingresults)
    {
        return handlingresultsMapper.insertHandlingresults(handlingresults);
    }

    /**
     * 修改投诉处理结果
     * 
     * @param handlingresults 投诉处理结果
     * @return 结果
     */
    @Override
    public int updateHandlingresults(Handlingresults handlingresults)
    {
        return handlingresultsMapper.updateHandlingresults(handlingresults);
    }

    /**
     * 批量删除投诉处理结果
     * 
     * @param ids 需要删除的投诉处理结果主键
     * @return 结果
     */
    @Override
    public int deleteHandlingresultsByIds(Long[] ids)
    {
        return handlingresultsMapper.deleteHandlingresultsByIds(ids);
    }

    /**
     * 删除投诉处理结果信息
     * 
     * @param id 投诉处理结果主键
     * @return 结果
     */
    @Override
    public int deleteHandlingresultsById(Long id)
    {
        return handlingresultsMapper.deleteHandlingresultsById(id);
    }
}
